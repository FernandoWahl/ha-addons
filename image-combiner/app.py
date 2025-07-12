from flask import Flask, request, jsonify, send_file
import requests
from PIL import Image
import io
import os
from typing import List
import tempfile

app = Flask(__name__)

class ImageCombiner:
    def __init__(self):
        # Get configuration from environment variables (set by Home Assistant)
        self.max_images = int(os.getenv('MAX_IMAGES', 4))
        self.image_quality = int(os.getenv('IMAGE_QUALITY', 85))
        self.cell_width = int(os.getenv('CELL_WIDTH', 400))
        self.cell_height = int(os.getenv('CELL_HEIGHT', 300))
        self.timeout = int(os.getenv('TIMEOUT', 10))
    
    def download_image(self, url: str) -> Image.Image:
        """Baixa uma imagem de uma URL e retorna um objeto PIL Image"""
        try:
            response = requests.get(url, timeout=10)
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
    
    def combine_images(self, image_urls: List[str]) -> Image.Image:
        """Combina as imagens em uma única imagem"""
        if not image_urls:
            raise ValueError("Lista de URLs não pode estar vazia")
        
        if len(image_urls) > self.max_images:
            raise ValueError(f"Máximo de {self.max_images} imagens permitidas")
        
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
            return images[0]
        elif num_images == 2:
            # Layout horizontal: 2x1
            grid_cols, grid_rows = 2, 1
        elif num_images == 3:
            # Layout: 2x2 com uma posição vazia
            grid_cols, grid_rows = 2, 2
        else:  # 4 imagens
            # Layout: 2x2
            grid_cols, grid_rows = 2, 2
        
        # Define o tamanho de cada célula da grade
        cell_width = 400
        cell_height = 300
        
        # Cria a imagem final
        final_width = grid_cols * cell_width
        final_height = grid_rows * cell_height
        combined_image = Image.new('RGB', (final_width, final_height), 'white')
        
        # Posiciona as imagens na grade
        for i, img in enumerate(images):
            # Redimensiona a imagem para caber na célula
            resized_img = self.resize_image_to_fit(img, cell_width, cell_height)
            
            # Calcula a posição na grade
            col = i % grid_cols
            row = i // grid_cols
            
            # Calcula a posição de colagem (centralizada na célula)
            x = col * cell_width + (cell_width - resized_img.width) // 2
            y = row * cell_height + (cell_height - resized_img.height) // 2
            
            # Cola a imagem na posição calculada
            combined_image.paste(resized_img, (x, y))
        
        return combined_image

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
        if len(urls) > 4:
            return jsonify({'error': 'Máximo de 4 URLs permitidas'}), 400
        
        # Combina as imagens
        combined_image = combiner.combine_images(urls)
        
        # Salva a imagem em um buffer
        img_buffer = io.BytesIO()
        combined_image.save(img_buffer, format='JPEG', quality=85)
        img_buffer.seek(0)
        
        return send_file(
            img_buffer,
            mimetype='image/jpeg',
            as_attachment=False,
            download_name='combined_image.jpg'
        )
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de health check"""
    return jsonify({'status': 'healthy', 'service': 'Image Combiner'})

@app.route('/', methods=['GET'])
def home():
    """Endpoint de informações da API"""
    return jsonify({
        'service': 'Image Combiner API',
        'version': '1.0.0',
        'endpoints': {
            'POST /combine': 'Combina até 4 imagens em uma única imagem',
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
            'response': 'Imagem JPEG combinada'
        }
    })

if __name__ == '__main__':
    import logging
    import os
    
    # Suprimir avisos do Werkzeug (servidor Flask de desenvolvimento)
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    
    # Log startup information
    print(f"🚀 Starting Image Combiner API")
    print(f"📊 Configuration:")
    print(f"   - Max images: {combiner.max_images}")
    print(f"   - Image quality: {combiner.image_quality}")
    print(f"   - Cell dimensions: {combiner.cell_width}x{combiner.cell_height}")
    print(f"   - Timeout: {combiner.timeout}s")
    print(f"🌐 Server starting on http://0.0.0.0:5000")
    
    # Detecta se está rodando no Home Assistant
    is_addon = os.getenv('HASSIO_TOKEN') is not None
    if is_addon:
        print("🏠 Running as Home Assistant Addon")
    
    app.run(debug=False, host='0.0.0.0', port=5000, use_reloader=False)
