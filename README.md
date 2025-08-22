# Image Combiner Home Assistant Addon

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]
![Supports armhf Architecture][armhf-shield]
![Supports armv7 Architecture][armv7-shield]
![Supports i386 Architecture][i386-shield]

Um addon do Home Assistant que fornece uma API HTTP para combinar até 4 imagens em uma única imagem composta.

## Sobre

Este addon transforma seu Home Assistant em um servidor de combinação de imagens, permitindo que você:

- ✅ Combine até 4 imagens em uma única imagem
- ✅ Configure qualidade, dimensões e timeout
- ✅ Use em automações do Home Assistant
- ✅ Acesse via API REST
- ✅ Suporte a múltiplos formatos de imagem

## Instalação

1. **Adicione este repositório ao Home Assistant:**
   - Vá para **Supervisor → Add-on Store**
   - Clique nos três pontos no canto superior direito
   - Selecione **Repositories**
   - Adicione: `https://github.com/FernandoWahl/ha-addons`

2. **Instale o addon:**
   - Encontre "Image Combiner" na lista de addons
   - Clique em **Install**

3. **Configure e inicie:**
   - Configure as opções conforme necessário
   - Clique em **Start**

## Configuração

```yaml
max_images: 4          # Máximo de imagens (1-4)
image_quality: 85      # Qualidade JPEG (50-100)
cell_width: 400        # Largura da célula (200-800px)
cell_height: 300       # Altura da célula (200-600px)
timeout: 10           # Timeout de download (5-30s)
```

## Uso

### API Endpoints

- **POST** `/combine` - Combina imagens
- **GET** `/health` - Health check
- **GET** `/` - Informações da API

### Exemplo de requisição

```bash
curl -X POST http://homeassistant.local:5000/combine \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://example.com/image1.jpg", "https://example.com/image2.jpg"]}' \
  --output combined.jpg
```

### Integração com Home Assistant

#### Automação
```yaml
automation:
  - alias: "Combinar câmeras"
    trigger:
      platform: time
      at: "08:00:00"
    action:
      service: rest_command.combine_images
      data:
        urls:
          - "http://camera1/snapshot.jpg"
          - "http://camera2/snapshot.jpg"
```

#### REST Command
```yaml
rest_command:
  combine_images:
    url: "http://localhost:5000/combine"
    method: POST
    headers:
      Content-Type: "application/json"
    payload: '{"urls": {{ urls | to_json }}}'
```

## Layout das Imagens

- **1 imagem**: Original
- **2 imagens**: Horizontal (2x1)
- **3-4 imagens**: Grade 2x2

## Funcionalidades

- 🖼️ Combina até 4 imagens automaticamente
- 📐 Redimensiona mantendo proporções
- ⚙️ Configurações personalizáveis
- 🏠 Integração nativa com Home Assistant
- 🌐 API REST completa
- 🔧 Suporte multi-arquitetura
- 📝 Logs detalhados
- ✅ Health checks automáticos

## Suporte

- [Documentação completa](DOCS.md)
- [Changelog](CHANGELOG.md)
- [Issues no GitHub][issues]

## Contribuição

Contribuições são bem-vindas! Por favor, leia as diretrizes de contribuição antes de enviar um PR.

## Licença

MIT License - veja [LICENSE](LICENSE) para detalhes.

---

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[armhf-shield]: https://img.shields.io/badge/armhf-yes-green.svg
[armv7-shield]: https://img.shields.io/badge/armv7-yes-green.svg
[i386-shield]: https://img.shields.io/badge/i386-yes-green.svg
[commits-shield]: https://img.shields.io/github/commit-activity/y/FernandoWahl/ha-addons.svg
[commits]: https://github.com/FernandoWahl/ha-addons/commits/main
[license-shield]: https://img.shields.io/github/license/FernandoWahl/ha-addons.svg
[releases-shield]: https://img.shields.io/github/release/FernandoWahl/ha-addons.svg
[releases]: https://github.com/FernandoWahl/ha-addons/releases
[issues]: https://github.com/FernandoWahl/ha-addons/issues
