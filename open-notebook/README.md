# Home Assistant Add-on: Open Notebook

![Supports aarch64 Architecture][aarch64-shield] ![Supports amd64 Architecture][amd64-shield]

Uma alternativa open source e focada em privacidade ao Google Notebook LM para pesquisa e anotações.

## Sobre

Open Notebook é um assistente de pesquisa poderoso que permite:

- 🔒 **Controlar seus dados** - Mantenha sua pesquisa privada e segura
- 🧠 **Insights com IA** - Obtenha resumos e análises inteligentes
- 📚 **Múltiplas fontes** - Importe PDFs, arquivos de texto, conteúdo web e podcasts
- 🎙️ **Integração com podcasts** - Transcreva e analise episódios de podcast
- 💬 **Chat interativo** - Faça perguntas sobre seus materiais de pesquisa
- 🔍 **Busca inteligente** - Encontre informações relevantes em todas as suas fontes
- 📝 **Anotações** - Crie e organize seus pensamentos e insights

## Instalação

1. Adicione este repositório ao Home Assistant
2. Instale o addon "Open Notebook"
3. Configure suas chaves de API de IA
4. Inicie o addon
5. Acesse através do botão "Open Web UI"

## Configuração Mínima

```yaml
# Configure pelo menos um provedor de IA
openai_api_key: "sua-chave-openai"
# OU
anthropic_api_key: "sua-chave-anthropic"
# OU
groq_api_key: "sua-chave-groq"

# Configurações básicas
database_url: "memory"
debug: false
```

## Funcionalidades

### Processamento de Documentos
- Extração e análise de texto de PDFs
- Scraping de conteúdo de páginas web
- Processamento de arquivos Markdown e texto
- Suporte a documentos Microsoft Word

### Integração com IA
- Suporte a múltiplos provedores de IA
- Resumos inteligentes de documentos
- Respostas a perguntas sobre fontes
- Respostas conscientes do contexto

### Suporte a Podcasts
- Transcrição automática
- Análise e insights de episódios
- Identificação de palestrantes
- Transcrições pesquisáveis

### Gerenciamento de Dados
- Armazenamento persistente no Home Assistant
- Capacidades de exportação
- Funcionalidade de backup e restauração
- Design focado em privacidade

## Uso

1. **Acesse a Interface**: Clique em "Open Web UI" para acessar o Open Notebook
2. **Configure Modelos de IA**: Vá para a página de Modelos para configurar seus provedores de IA
3. **Adicione Fontes**: Faça upload de documentos, adicione URLs web ou importe podcasts
4. **Crie Notebooks**: Organize sua pesquisa em notebooks temáticos
5. **Faça Perguntas**: Use a interface de chat para consultar seus materiais de pesquisa
6. **Tome Notas**: Adicione seus próprios insights e observações

## Suporte

- [Repositório GitHub](https://github.com/lfnovo/open-notebook)
- [Comunidade Discord](https://discord.gg/37XJPXfz2w)
- [Documentação](https://www.open-notebook.ai)

## Licença

Este projeto está licenciado sob a Licença MIT.

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
