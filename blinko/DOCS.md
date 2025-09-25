# Blinko Add-on

## Sobre

Blinko é uma aplicação de anotações com IA que permite capturar e organizar pensamentos rapidamente. Este add-on executa o Blinko como um submodulo Git, facilitando atualizações automáticas.

## Funcionalidades

- 🤖 **IA integrada** para busca semântica (RAG)
- 📝 **Editor rico** com Markdown
- 🏷️ **Sistema de tags** inteligente
- 📎 **Anexos** (imagens, áudio, arquivos)
- 🔍 **Busca avançada** com embeddings
- 💬 **Chat com IA** sobre suas notas
- 📊 **Analytics** e visualizações
- 🎙️ **Gravação de áudio** com transcrição
- 📷 **Captura de imagens**
- 🌐 **Interface multilíngue**

## Configuração

### Banco de Dados
```yaml
database_url: "postgresql://usuario:senha@host:5432/database"
```

### Chaves de API (opcional)
Configure pelo menos uma para usar funcionalidades de IA:

```yaml
openai_api_key: "sk-..."
anthropic_api_key: "sk-ant-..."
groq_api_key: "gsk_..."
```

### Configurações Avançadas
```yaml
debug: false
log_level: "INFO"  # DEBUG, INFO, WARN, ERROR
```

## Uso

1. **Configure o banco de dados** PostgreSQL
2. **Adicione chaves de API** para funcionalidades de IA
3. **Inicie o add-on**
4. **Acesse via Web UI** ou painel do Home Assistant

## Integração com Home Assistant

### Sensor de Status
```yaml
sensor:
  - platform: rest
    name: "Blinko Status"
    resource: "http://localhost:3000/api/health"
    method: GET
    value_template: "{{ value_json.status }}"
```

### Automação de Backup
```yaml
automation:
  - alias: "Backup Blinko"
    trigger:
      platform: time
      at: "02:00:00"
    action:
      service: shell_command.backup_blinko
```

## Atualizações

O add-on atualiza automaticamente o código do Blinko a cada reinicialização, puxando a versão mais recente do repositório oficial.

## Suporte

- [Repositório Oficial do Blinko](https://github.com/blinko-space/blinko)
- [Documentação Oficial](https://docs.blinko.space/)
- [Issues](https://github.com/FernandoWahl/ha-addons/issues)
