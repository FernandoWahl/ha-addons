# Image Combiner Home Assistant Addon

Este addon fornece uma API HTTP que combina até 4 imagens em uma única imagem composta, com cache Redis para melhor performance.

## Instalação

1. Adicione este repositório aos seus repositórios de addon do Home Assistant
2. Instale o addon "Image Combiner"
3. Configure as opções conforme necessário
4. Inicie o addon

## Configuração

### Opções disponíveis:

#### Configurações de Imagem:
- **max_images** (1-4): Número máximo de imagens que podem ser combinadas
- **image_quality** (50-100): Qualidade JPEG da imagem final
- **cell_width** (200-800): Largura de cada célula da grade em pixels
- **cell_height** (200-600): Altura de cada célula da grade em pixels
- **timeout** (5-30): Tempo limite para download de cada imagem em segundos

#### Configurações de Cache Redis:
- **redis_host**: Endereço do servidor Redis (padrão: localhost)
- **redis_port** (1-65535): Porta do servidor Redis (padrão: 6379)
- **redis_password**: Senha do Redis (opcional)
- **cache_ttl** (60-3600): Tempo de vida do cache em segundos (padrão: 600)
- **enable_cache**: Habilita/desabilita o cache Redis (padrão: true)

### Configuração padrão:
```yaml
max_images: 4
image_quality: 85
cell_width: 400
cell_height: 300
timeout: 10
redis_host: "localhost"
redis_port: 6379
redis_password: ""
cache_ttl: 600
enable_cache: true
```

## Funcionalidades do Cache

### Como funciona:
1. **Chave única**: Cada combinação de URLs + configurações gera uma chave MD5 única
2. **Compressão gzip**: Imagens são comprimidas antes de serem armazenadas
3. **TTL automático**: Cache expira automaticamente após o tempo configurado
4. **Fallback gracioso**: Se Redis não estiver disponível, funciona sem cache

### Benefícios:
- ✅ **Performance**: Imagens idênticas são servidas instantaneamente do cache
- ✅ **Economia de banda**: Reduz downloads desnecessários
- ✅ **Compressão**: Economiza espaço no Redis (até 70% de redução)
- ✅ **Configurável**: TTL e configurações ajustáveis

## Uso

### Endpoints disponíveis:

#### POST /combine
Combina imagens em uma única imagem (com cache automático).

**URL:** `http://homeassistant.local:5000/combine`

**Request:**
```json
{
  "urls": [
    "https://exemplo.com/imagem1.jpg",
    "https://exemplo.com/imagem2.jpg"
  ]
}
```

**Response:** Imagem JPEG combinada

#### GET /cache/stats
Retorna estatísticas do cache Redis.

**Response:**
```json
{
  "enabled": true,
  "total_keys": 15,
  "memory_used": "2.1M",
  "connected_clients": 1,
  "ttl_seconds": 600
}
```

#### POST /cache/clear
Limpa todas as imagens do cache.

**Response:**
```json
{
  "message": "15 chaves removidas do cache",
  "deleted_keys": 15
}
```

#### GET /health
Health check do serviço com informações de cache.

#### GET /
Informações da API e configuração atual.

### Exemplo de uso em automações do Home Assistant

```yaml
# automation.yaml
- alias: "Combinar imagens das câmeras"
  trigger:
    - platform: time
      at: "08:00:00"
  action:
    - service: rest_command.combine_camera_images
      data:
        urls:
          - "http://192.168.1.100/camera1/snapshot.jpg"
          - "http://192.168.1.101/camera2/snapshot.jpg"
          - "http://192.168.1.102/camera3/snapshot.jpg"
```

```yaml
# configuration.yaml
rest_command:
  combine_camera_images:
    url: "http://localhost:5000/combine"
    method: POST
    headers:
      Content-Type: "application/json"
    payload: '{"urls": {{ urls | to_json }}}'
```

### Exemplo com curl

```bash
curl -X POST http://homeassistant.local:5000/combine \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://picsum.photos/400/300?random=1", "https://picsum.photos/400/300?random=2"]}' \
  --output combined_image.jpg
```

## Layout das imagens

O sistema organiza as imagens automaticamente:

- **1 imagem**: Imagem original
- **2 imagens**: Layout horizontal (2x1)
- **3 imagens**: Layout em grade 2x2 (com uma posição vazia)
- **4 imagens**: Layout em grade 2x2

## Configuração do Redis

### Redis local (recomendado):
```yaml
redis_host: "localhost"
redis_port: 6379
redis_password: ""
enable_cache: true
```

### Redis externo:
```yaml
redis_host: "192.168.1.100"
redis_port: 6379
redis_password: "sua_senha_aqui"
enable_cache: true
```

### Desabilitar cache:
```yaml
enable_cache: false
```

## Monitoramento

### Logs do cache:
```
✅ Redis connected: localhost:6379
🎯 Cache HIT: a1b2c3d4e5f6...
💾 Cache STORED: a1b2c3d4e5f6...
📊 Compression: 45678 → 15234 bytes (66.7% saved)
```

### Estatísticas via API:
```bash
curl http://homeassistant.local:5000/cache/stats
```

## Integração com Home Assistant

### Camera Entity
```yaml
# configuration.yaml
camera:
  - platform: generic
    name: "Combined Cameras"
    still_image_url: "http://localhost:5000/combine"
    content_type: "image/jpeg"
```

### Sensor para monitoramento
```yaml
# configuration.yaml
sensor:
  - platform: rest
    name: "Image Combiner Cache"
    resource: "http://localhost:5000/cache/stats"
    value_template: "{{ value_json.total_keys }}"
    json_attributes:
      - enabled
      - memory_used
      - ttl_seconds
```

## Troubleshooting

### Cache não funciona:
1. Verifique se Redis está rodando
2. Confirme host/porta/senha do Redis
3. Verifique logs do addon
4. Teste conectividade: `redis-cli ping`

### Performance:
1. Ajuste `cache_ttl` conforme necessário
2. Monitore uso de memória do Redis
3. Use `POST /cache/clear` se necessário

### Problemas comuns:
1. **Timeout de download**: Aumente o valor de `timeout`
2. **Imagens muito grandes**: Ajuste `cell_width` e `cell_height`
3. **Qualidade baixa**: Aumente o valor de `image_quality`
4. **Cache cheio**: Reduza `cache_ttl` ou limpe o cache

## Limitações

- Máximo de 4 URLs por requisição
- URLs devem retornar imagens válidas
- Suporte a formatos: JPEG, PNG, GIF, BMP, etc.
- Conversão automática para RGB
- Cache requer Redis disponível

## Segurança

- O addon roda em modo não privilegiado
- Cache usa chaves MD5 para privacidade
- Senhas Redis são opcionais
- TTL automático previne acúmulo de dados
