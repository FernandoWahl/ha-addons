from flask import Flask, request, jsonify, send_file
import requests
from PIL import Image
import io
import os
import gzip
import hashlib
import json
from typing import List, Optional
import redis
from redis.exceptions import ConnectionError as RedisConnectionError

app = Flask(__name__)

class RedisCache:
    def __init__(self, host: str, port: int, password: str = None, ttl: int = 600):
        """Inicializa conexão com Redis"""
        self.ttl = ttl
        self.enabled = True
        
        try:
            self.redis_client = redis.Redis(
                host=host,
                port=port,
                password=password if password else None,
                decode_responses=False,  # Para trabalhar com dados binários
                socket_connect_timeout=5,
                socket_timeout=5
            )
            # Testa a conexão
            self.redis_client.ping()
            print(f"✅ Redis connected: {host}:{port}")
        except (RedisConnectionError, Exception) as e:
            print(f"⚠️ Redis connection failed: {e}")
            print("📝 Cache disabled - images will not be cached")
            self.enabled = False
            self.redis_client = None
    
    def _generate_key(self, urls: List[str], config: dict) -> str:
        """Gera uma chave única baseada nas URLs e configurações"""
        # Cria um hash das URLs e configurações
        data = {
            'urls': sorted(urls),  # Ordena para consistência
            'config': config
        }
        data_str = json.dumps(data, sort_keys=True)
        return f"image_combiner:{hashlib.md5(data_str.encode()).hexdigest()}"
    
    def get_cached_image(self, urls: List[str], config: dict) -> Optional[bytes]:
        """Recupera imagem do cache"""
        if not self.enabled:
            return None
            
        try:
            key = self._generate_key(urls, config)
            compressed_data = self.redis_client.get(key)
            
            if compressed_data:
                # Descomprime os dados
                image_data = gzip.decompress(compressed_data)
                print(f"🎯 Cache HIT: {key[:16]}...")
                return image_data
            else:
                print(f"❌ Cache MISS: {key[:16]}...")
                return None
                
        except Exception as e:
            print(f"⚠️ Cache get error: {e}")
            return None
    
    def cache_image(self, urls: List[str], config: dict, image_data: bytes) -> bool:
        """Armazena imagem no cache com compressão"""
        if not self.enabled:
            return False
            
        try:
            key = self._generate_key(urls, config)
            
            # Comprime os dados da imagem
            compressed_data = gzip.compress(image_data, compresslevel=6)
            
            # Armazena no Redis com TTL
            self.redis_client.setex(key, self.ttl, compressed_data)
            
            # Calcula estatísticas de compressão
            original_size = len(image_data)
            compressed_size = len(compressed_data)
            compression_ratio = (1 - compressed_size / original_size) * 100
            
            print(f"💾 Cache STORED: {key[:16]}...")
            print(f"📊 Compression: {original_size} → {compressed_size} bytes ({compression_ratio:.1f}% saved)")
            
            return True
            
        except Exception as e:
            print(f"⚠️ Cache store error: {e}")
            return False
    
    def get_cache_stats(self) -> dict:
        """Retorna estatísticas do cache"""
        if not self.enabled:
            return {"enabled": False, "message": "Redis not available"}
            
        try:
            info = self.redis_client.info()
            keys = self.redis_client.keys("image_combiner:*")
            
            return {
                "enabled": True,
                "total_keys": len(keys),
                "memory_used": info.get('used_memory_human', 'N/A'),
                "connected_clients": info.get('connected_clients', 0),
                "ttl_seconds": self.ttl
            }
        except Exception as e:
            return {"enabled": False, "error": str(e)}

class ImageCombiner:
    def __init__(self):
        # Get configuration from environment variables (set by Home Assistant)
        self.max_images = int(os.getenv('MAX_IMAGES', 4))
        self.image_quality = int(os.getenv('IMAGE_QUALITY', 85))
        self.cell_width = int(os.getenv('CELL_WIDTH', 400))
        self.cell_height = int(os.getenv('CELL_HEIGHT', 300))
        self.timeout = int(os.getenv('TIMEOUT', 10))
        
        # Redis configuration
        redis_host = os.getenv('REDIS_HOST', 'localhost')
        redis_port = int(os.getenv('REDIS_PORT', 6379))
        redis_password = os.getenv('REDIS_PASSWORD', '')
        cache_ttl = int(os.getenv('CACHE_TTL', 600))
        enable_cache = os.getenv('ENABLE_CACHE', 'true').lower() == 'true'
        
        # Initialize Redis cache
        if enable_cache:
            self.cache = RedisCache(redis_host, redis_port, redis_password, cache_ttl)
        else:
            print("📝 Cache disabled by configuration")
            self.cache = RedisCache("", 0)  # Disabled cache
            self.cache.enabled = False
    
    def get_config_dict(self) -> dict:
        """Retorna configuração atual como dicionário para cache key"""
        return {
            'image_quality': self.image_quality,
            'cell_width': self.cell_width,
            'cell_height': self.cell_height,
            'max_images': self.max_images
        }
    
    def download_image(self, url: str) -> Image.Image:
        """Baixa uma imagem de uma URL e retorna um objeto PIL Image"""
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            return Image.open(io.BytesIO(response.content))
        except Exception as e:
            raise Exception(f"Erro ao baixar imagem de {url}: {str(e)}")
    
    def resize_image_to_fit(self, image: Image.Image, target_width: int, target_height: int) -> Image.Image:
        """Redimensiona a imagem mantendo a proporção para caber no espaço alvo"""
        # Calcula a proporção para manter aspect ratio
        img_ratio = image.width / image.height
        target_ratio = target_width / target_height
        
        if img_ratio > target_ratio:
            # Imagem é mais larga, ajustar pela largura
            new_width = target_width
            new_height = int(target_width / img_ratio)
        else:
            # Imagem é mais alta, ajustar pela altura
            new_height = target_height
            new_width = int(target_height * img_ratio)
        
        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    def combine_images(self, image_urls: List[str]) -> bytes:
        """Combina as imagens em uma única imagem e retorna os bytes"""
        if not image_urls:
            raise ValueError("Lista de URLs não pode estar vazia")
        
        if len(image_urls) > self.max_images:
            raise ValueError(f"Máximo de {self.max_images} imagens permitidas")
        
        # Verifica cache primeiro
        config = self.get_config_dict()
        cached_image = self.cache.get_cached_image(image_urls, config)
        if cached_image:
            return cached_image
        
        # Baixa todas as imagens
        images = []
        for url in image_urls:
            img = self.download_image(url)
            # Converte para RGB se necessário (para evitar problemas com PNG transparente)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            images.append(img)
        
        num_images = len(images)
        
        # Define o layout baseado no número de imagens
        if num_images == 1:
            combined_image = images[0]
        else:
            if num_images == 2:
                # Layout horizontal: 2x1
                grid_cols, grid_rows = 2, 1
            elif num_images == 3:
                # Layout: 2x2 com uma posição vazia
                grid_cols, grid_rows = 2, 2
            else:  # 4 imagens
                # Layout: 2x2
                grid_cols, grid_rows = 2, 2
            
            # Cria a imagem final
            final_width = grid_cols * self.cell_width
            final_height = grid_rows * self.cell_height
            combined_image = Image.new('RGB', (final_width, final_height), 'white')
            
            # Posiciona as imagens na grade
            for i, img in enumerate(images):
                # Redimensiona a imagem para caber na célula
                resized_img = self.resize_image_to_fit(img, self.cell_width, self.cell_height)
                
                # Calcula a posição na grade
                col = i % grid_cols
                row = i // grid_cols
                
                # Calcula a posição de colagem (centralizada na célula)
                x = col * self.cell_width + (self.cell_width - resized_img.width) // 2
                y = row * self.cell_height + (self.cell_height - resized_img.height) // 2
                
                # Cola a imagem na posição calculada
                combined_image.paste(resized_img, (x, y))
        
        # Converte para bytes
        img_buffer = io.BytesIO()
        combined_image.save(img_buffer, format='JPEG', quality=self.image_quality)
        image_data = img_buffer.getvalue()
        
        # Armazena no cache
        self.cache.cache_image(image_urls, config, image_data)
        
        return image_data

# Instância do combinador de imagens
combiner = ImageCombiner()

@app.route('/combine', methods=['POST'])
def combine_images():
    """Endpoint para combinar imagens"""
    try:
        # Verifica se o JSON foi enviado
        if not request.is_json:
            return jsonify({'error': 'Content-Type deve ser application/json'}), 400
        
        data = request.get_json()
        
        # Verifica se o parâmetro 'urls' existe
        if 'urls' not in data:
            return jsonify({'error': 'Parâmetro "urls" é obrigatório'}), 400
        
        urls = data['urls']
        
        # Valida se é uma lista
        if not isinstance(urls, list):
            return jsonify({'error': 'Parâmetro "urls" deve ser uma lista'}), 400
        
        # Valida se não está vazia
        if not urls:
            return jsonify({'error': 'Lista de URLs não pode estar vazia'}), 400
        
        # Valida o limite de URLs
        if len(urls) > combiner.max_images:
            return jsonify({'error': f'Máximo de {combiner.max_images} URLs permitidas'}), 400
        
        # Combina as imagens (com cache automático)
        image_data = combiner.combine_images(urls)
        
        # Retorna a imagem
        return send_file(
            io.BytesIO(image_data),
            mimetype='image/jpeg',
            as_attachment=False,
            download_name='combined_image.jpg'
        )
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@app.route('/cache/stats', methods=['GET'])
def cache_stats():
    """Endpoint para estatísticas do cache"""
    stats = combiner.cache.get_cache_stats()
    return jsonify(stats)

@app.route('/cache/clear', methods=['POST'])
def clear_cache():
    """Endpoint para limpar o cache"""
    try:
        if not combiner.cache.enabled:
            return jsonify({'error': 'Cache não está habilitado'}), 400
        
        # Remove todas as chaves do cache do image combiner
        keys = combiner.cache.redis_client.keys("image_combiner:*")
        if keys:
            deleted = combiner.cache.redis_client.delete(*keys)
            return jsonify({
                'message': f'{deleted} chaves removidas do cache',
                'deleted_keys': deleted
            })
        else:
            return jsonify({'message': 'Cache já estava vazio'})
            
    except Exception as e:
        return jsonify({'error': f'Erro ao limpar cache: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de health check"""
    cache_stats = combiner.cache.get_cache_stats()
    
    return jsonify({
        'status': 'healthy', 
        'service': 'Image Combiner',
        'version': '1.1.0',
        'config': {
            'max_images': combiner.max_images,
            'image_quality': combiner.image_quality,
            'cell_dimensions': f'{combiner.cell_width}x{combiner.cell_height}',
            'timeout': combiner.timeout
        },
        'cache': cache_stats
    })

@app.route('/', methods=['GET'])
def home():
    """Endpoint de informações da API"""
    return jsonify({
        'service': 'Image Combiner API',
        'version': '1.1.0',
        'home_assistant_addon': True,
        'features': ['image_combination', 'redis_cache', 'compression'],
        'config': {
            'max_images': combiner.max_images,
            'image_quality': combiner.image_quality,
            'cell_width': combiner.cell_width,
            'cell_height': combiner.cell_height,
            'timeout': combiner.timeout,
            'cache_enabled': combiner.cache.enabled,
            'cache_ttl': combiner.cache.ttl if combiner.cache.enabled else None
        },
        'endpoints': {
            'POST /combine': 'Combina até 4 imagens em uma única imagem (com cache)',
            'GET /cache/stats': 'Estatísticas do cache Redis',
            'POST /cache/clear': 'Limpa o cache Redis',
            'GET /health': 'Health check do serviço',
            'GET /': 'Informações da API'
        },
        'usage': {
            'method': 'POST',
            'url': '/combine',
            'content_type': 'application/json',
            'body': {
                'urls': ['url1', 'url2', 'url3', 'url4']
            },
            'response': 'Imagem JPEG combinada (possivelmente do cache)'
        }
    })

if __name__ == '__main__':
    import logging
    import os
    
    # Suprimir avisos do Werkzeug (servidor Flask de desenvolvimento)
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    
    # Log startup information
    print(f"🚀 Starting Image Combiner API v1.1.0")
    print(f"📊 Configuration:")
    print(f"   - Max images: {combiner.max_images}")
    print(f"   - Image quality: {combiner.image_quality}")
    print(f"   - Cell dimensions: {combiner.cell_width}x{combiner.cell_height}")
    print(f"   - Timeout: {combiner.timeout}s")
    print(f"💾 Cache: {'Enabled' if combiner.cache.enabled else 'Disabled'}")
    if combiner.cache.enabled:
        print(f"   - TTL: {combiner.cache.ttl}s")
        print(f"   - Compression: gzip level 6")
    print(f"🌐 Server starting on http://0.0.0.0:5000")
    
    # Detecta se está rodando no Home Assistant
    is_addon = os.getenv('HASSIO_TOKEN') is not None
    if is_addon:
        print("🏠 Running as Home Assistant Addon")
    
    app.run(debug=False, host='0.0.0.0', port=5000, use_reloader=False)
