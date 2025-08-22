# Home Assistant Add-on: Open Notebook

![Supports aarch64 Architecture][aarch64-shield] ![Supports amd64 Architecture][amd64-shield]

An open source, privacy-focused alternative to Google's Notebook LM for research and note-taking.

## About

Open Notebook is a powerful research assistant that allows you to:

- 🔒 **Control your data** - Keep your research private and secure
- 🧠 **AI-powered insights** - Get intelligent summaries and analysis
- 📚 **Multiple sources** - Import PDFs, text files, web content, and podcasts
- 🎙️ **Podcast integration** - Transcribe and analyze podcast episodes
- 💬 **Interactive chat** - Ask questions about your research materials
- 🔍 **Smart search** - Find relevant information across all your sources
- 📝 **Note-taking** - Create and organize your thoughts and insights

## Installation

1. Add this repository to your Home Assistant add-on store
2. Install the "Open Notebook" add-on
3. Configure the add-on (see configuration section below)
4. Start the add-on
5. Access the web interface through the "Open Web UI" button

## Configuration

### Basic Configuration

```yaml
database_url: "memory"
database_user: "root"
database_password: "root"
debug: false
log_level: "INFO"
```

### AI Model Configuration

Configure at least one AI provider to use Open Notebook:

```yaml
# OpenAI
openai_api_key: "your-openai-api-key"

# Anthropic (Claude)
anthropic_api_key: "your-anthropic-api-key"

# Groq
groq_api_key: "your-groq-api-key"

# Google AI
google_api_key: "your-google-api-key"

# Mistral AI
mistral_api_key: "your-mistral-api-key"

# DeepSeek
deepseek_api_key: "your-deepseek-api-key"

# Ollama (for local models)
ollama_base_url: "http://your-ollama-server:11434"
```

### File Upload Settings

```yaml
max_file_size: 50  # Maximum file size in MB
allowed_file_types:
  - "pdf"
  - "txt"
  - "md"
  - "docx"
  - "html"
```

### Security (Optional)

```yaml
enable_auth: true
auth_username: "your-username"
auth_password: "your-password"
```

## Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `database_url` | string | `memory` | Database connection URL |
| `database_user` | string | `root` | Database username |
| `database_password` | string | `root` | Database password |
| `openai_api_key` | string | - | OpenAI API key |
| `anthropic_api_key` | string | - | Anthropic API key |
| `groq_api_key` | string | - | Groq API key |
| `google_api_key` | string | - | Google AI API key |
| `mistral_api_key` | string | - | Mistral AI API key |
| `deepseek_api_key` | string | - | DeepSeek API key |
| `ollama_base_url` | string | - | Ollama server URL |
| `debug` | boolean | `false` | Enable debug mode |
| `log_level` | list | `INFO` | Log level (DEBUG, INFO, WARNING, ERROR) |
| `max_file_size` | integer | `50` | Maximum file size in MB |
| `allowed_file_types` | list | See above | Allowed file extensions |
| `enable_auth` | boolean | `false` | Enable authentication |
| `auth_username` | string | - | Authentication username |
| `auth_password` | string | - | Authentication password |

## Usage

1. **Access the Interface**: Click "Open Web UI" to access Open Notebook
2. **Configure AI Models**: Go to the Models page to set up your AI providers
3. **Add Sources**: Upload documents, add web URLs, or import podcasts
4. **Create Notebooks**: Organize your research into themed notebooks
5. **Ask Questions**: Use the chat interface to query your research materials
6. **Take Notes**: Add your own insights and observations

## Features

### Document Processing
- PDF text extraction and analysis
- Web page content scraping
- Markdown and text file processing
- Microsoft Word document support

### AI Integration
- Multiple AI provider support
- Intelligent document summarization
- Question answering across sources
- Context-aware responses

### Podcast Support
- Automatic transcription
- Episode analysis and insights
- Speaker identification
- Searchable transcripts

### Data Management
- Persistent storage in Home Assistant
- Export capabilities
- Backup and restore functionality
- Privacy-focused design

## Troubleshooting

### Common Issues

1. **Add-on won't start**: Check the logs for configuration errors
2. **AI models not working**: Verify your API keys are correct
3. **File upload fails**: Check file size and type restrictions
4. **Database errors**: Ensure database configuration is correct

### Logs

Check the add-on logs for detailed error information:
- Supervisor logs: `/app/logs/supervisord.log`
- API logs: `/app/logs/api_error.log` and `/app/logs/api_output.log`
- Streamlit logs: `/app/logs/streamlit_error.log` and `/app/logs/streamlit_output.log`

## Support

- [GitHub Repository](https://github.com/lfnovo/open-notebook)
- [Discord Community](https://discord.gg/37XJPXfz2w)
- [Documentation](https://www.open-notebook.ai)

## License

This project is licensed under the MIT License.

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
