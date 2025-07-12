# Image Combiner Home Assistant Addon

Este addon fornece uma API HTTP que combina até 4 imagens em uma única imagem composta, diretamente no seu Home Assistant.

## Instalação

1. Adicione este repositório aos seus repositórios de addon do Home Assistant
2. Instale o addon "Image Combiner"
3. Configure as opções conforme necessário
4. Inicie o addon

## Configuração

### Opções disponíveis:

- **max_images** (1-4): Número máximo de imagens que podem ser combinadas
- **image_quality** (50-100): Qualidade JPEG da imagem final
- **cell_width** (200-800): Largura de cada célula da grade em pixels
- **cell_height** (200-600): Altura de cada célula da grade em pixels
- **timeout** (5-30): Tempo limite para download de cada imagem em segundos

### Configuração padrão:
```yaml
max_images: 4
image_quality: 85
cell_width: 400
cell_height: 300
timeout: 10
```

## Uso

### Endpoints disponíveis:

#### POST /combine
Combina imagens em uma única imagem.

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

#### GET /health
Health check do serviço.

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

## Integração com Home Assistant

### Camera Entity
Você pode criar uma camera entity que usa o serviço:

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
    name: "Image Combiner Status"
    resource: "http://localhost:5000/health"
    value_template: "{{ value_json.status }}"
    json_attributes:
      - config
```

## Logs e troubleshooting

Os logs do addon podem ser visualizados na interface do Home Assistant em:
**Supervisor → Image Combiner → Logs**

### Problemas comuns:

1. **Timeout de download**: Aumente o valor de `timeout` na configuração
2. **Imagens muito grandes**: Ajuste `cell_width` e `cell_height`
3. **Qualidade baixa**: Aumente o valor de `image_quality`

## Limitações

- Máximo de 4 URLs por requisição
- URLs devem retornar imagens válidas
- Suporte a formatos: JPEG, PNG, GIF, BMP, etc.
- Conversão automática para RGB

## Segurança

- O addon roda em modo não privilegiado
- Não requer acesso à rede host
- Todas as configurações são validadas
- Timeout configurável para evitar travamentos
