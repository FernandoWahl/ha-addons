# Open Notebook Add-on for Home Assistant

![Open Notebook](https://raw.githubusercontent.com/lfnovo/open-notebook/main/docs/images/logo.png)

## About

This add-on provides a pure interface to the original [Open Notebook](https://github.com/lfnovo/open-notebook) project by lfnovo, with PostgreSQL database support for enhanced performance and scalability.

Open Notebook is a powerful AI-powered note-taking and knowledge management system that combines the best of traditional notebooks with modern AI capabilities.

## Features

- 🤖 **AI-Powered**: Integration with multiple AI providers (OpenAI, Anthropic, Groq, Google, Mistral, DeepSeek)
- 📝 **Smart Notes**: AI-enhanced note-taking with automatic tagging and organization
- 🔍 **Semantic Search**: Find information across your notes using natural language
- 🗄️ **PostgreSQL Support**: Robust database backend for better performance
- 📊 **Analytics**: Insights into your knowledge base and usage patterns
- 🔗 **Integrations**: Connect with various data sources and APIs
- 🎨 **Modern UI**: Clean, intuitive Streamlit-based interface

## Installation

1. Navigate to Supervisor → Add-on Store
2. Add this repository: `https://github.com/FernandoWahl/ha-addons`
3. Find "Open Notebook" in the add-on list
4. Click "Install"
5. Configure the add-on (see Configuration section)
6. Start the add-on

## Configuration

### Database Configuration

#### PostgreSQL (Recommended)
```yaml
database_type: "postgresql"
postgres_host: "your-postgres-host"
postgres_port: 5432
postgres_database: "open_notebook"
postgres_user: "open_notebook_user"
postgres_password: "your_secure_password"
```

#### SQLite (Fallback)
```yaml
database_type: "sqlite"
# No additional configuration needed
```

### AI Model Configuration

```yaml
# API Keys for AI providers
openai_api_key: "sk-..."
anthropic_api_key: "sk-ant-..."
groq_api_key: "gsk_..."
google_api_key: "AIza..."
mistral_api_key: "..."
deepseek_api_key: "..."

# Ollama (for local AI models)
ollama_base_url: "http://your-ollama-host:11434"
```

### Application Settings

```yaml
debug: false
log_level: "INFO"
max_file_size: 50
allowed_file_types: ["pdf", "txt", "md", "docx", "html"]

# Optional authentication
enable_auth: false
auth_username: ""
auth_password: ""
```

## Database Setup

### PostgreSQL Setup

1. **Create Database:**
   ```sql
   CREATE DATABASE open_notebook;
   ```

2. **Create User:**
   ```sql
   CREATE USER open_notebook_user WITH PASSWORD 'your_secure_password';
   GRANT ALL PRIVILEGES ON DATABASE open_notebook TO open_notebook_user;
   ```

3. **Configure Add-on:**
   - Set `database_type` to `postgresql`
   - Fill in your PostgreSQL connection details
   - Start the add-on

### SQLite Fallback

If PostgreSQL is not configured or connection fails, the add-on automatically falls back to SQLite:
- Data stored in `/data/open_notebook.db`
- Automatic creation and migration
- Suitable for smaller installations

## Usage

1. **Access the Interface:**
   - Web UI: `http://[HOST]:8501`
   - API: `http://[HOST]:8000`

2. **First Setup:**
   - Configure at least one AI provider API key
   - Create your first notebook
   - Start taking AI-enhanced notes

3. **Features:**
   - Create and organize notebooks
   - Use AI for note enhancement and generation
   - Search across your knowledge base
   - Analyze your notes and patterns

## Ports

- **8501/tcp**: Streamlit Web Interface
- **8000/tcp**: FastAPI Backend

## Data Persistence

- **PostgreSQL**: Data stored in your external PostgreSQL database
- **SQLite**: Data stored in `/data/open_notebook.db` (mapped to Home Assistant data directory)
- **Files**: Uploaded files stored in `/share/open-notebook/`

## AI Providers

### Supported Providers

- **OpenAI**: GPT-3.5, GPT-4, GPT-4 Turbo
- **Anthropic**: Claude 3 (Haiku, Sonnet, Opus)
- **Groq**: Fast inference for various models
- **Google**: Gemini Pro, Gemini Pro Vision
- **Mistral**: Mistral 7B, Mixtral 8x7B
- **DeepSeek**: DeepSeek Coder, DeepSeek Chat
- **Ollama**: Local models (Llama 2, Code Llama, etc.)

### API Key Setup

1. **OpenAI**: Get your API key from [OpenAI Platform](https://platform.openai.com/)
2. **Anthropic**: Get your API key from [Anthropic Console](https://console.anthropic.com/)
3. **Groq**: Get your API key from [Groq Console](https://console.groq.com/)
4. **Google**: Get your API key from [Google AI Studio](https://makersuite.google.com/)
5. **Ollama**: Set up [Ollama](https://ollama.ai/) on your network

## Troubleshooting

### Database Connection Issues

1. **PostgreSQL Connection Failed:**
   - Verify host, port, and credentials
   - Check network connectivity
   - Ensure database exists
   - Add-on will fall back to SQLite

2. **SQLite Issues:**
   - Check `/data` directory permissions
   - Ensure sufficient disk space

### AI Provider Issues

1. **API Key Errors:**
   - Verify API keys are correct
   - Check API quotas and billing
   - Ensure API keys have proper permissions

2. **Ollama Connection:**
   - Verify Ollama is running and accessible
   - Check firewall settings
   - Test connection from Home Assistant network

### Performance Issues

1. **Slow Response:**
   - Use PostgreSQL for better performance
   - Check AI provider response times
   - Monitor system resources

2. **Memory Usage:**
   - Adjust `max_file_size` setting
   - Monitor large file uploads
   - Consider system RAM limitations

## Support

- **Original Project**: [Open Notebook GitHub](https://github.com/lfnovo/open-notebook)
- **Add-on Issues**: [HA Add-ons Repository](https://github.com/FernandoWahl/ha-addons)
- **Documentation**: [Open Notebook Docs](https://github.com/lfnovo/open-notebook/tree/main/docs)

## License

This add-on is a pure interface to the original Open Notebook project. All credit goes to the original author lfnovo. The add-on wrapper is provided under the MIT License.

## Acknowledgments

- **lfnovo**: Original Open Notebook creator
- **Open Notebook Community**: Contributors and users
- **Home Assistant**: Platform and ecosystem
