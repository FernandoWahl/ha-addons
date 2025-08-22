#!/usr/bin/with-contenv bashio

echo "Starting Open Notebook..."

# Create directories
mkdir -p /config/open-notebook
mkdir -p /share/open-notebook
mkdir -p /app/logs

# Read configuration from Home Assistant
DATABASE_URL=$(bashio::config 'database_url' 'memory')
DATABASE_USER=$(bashio::config 'database_user' 'root')
DATABASE_PASSWORD=$(bashio::config 'database_password' 'root')
DEBUG=$(bashio::config 'debug' 'false')
LOG_LEVEL=$(bashio::config 'log_level' 'INFO')
MAX_FILE_SIZE=$(bashio::config 'max_file_size' '50')
ENABLE_AUTH=$(bashio::config 'enable_auth' 'false')

# AI API Keys
OPENAI_API_KEY=$(bashio::config 'openai_api_key' '')
ANTHROPIC_API_KEY=$(bashio::config 'anthropic_api_key' '')
GROQ_API_KEY=$(bashio::config 'groq_api_key' '')
GOOGLE_API_KEY=$(bashio::config 'google_api_key' '')
MISTRAL_API_KEY=$(bashio::config 'mistral_api_key' '')
DEEPSEEK_API_KEY=$(bashio::config 'deepseek_api_key' '')
OLLAMA_BASE_URL=$(bashio::config 'ollama_base_url' '')

# Authentication
AUTH_USERNAME=$(bashio::config 'auth_username' '')
AUTH_PASSWORD=$(bashio::config 'auth_password' '')

# Create environment file
cat > /app/.env << EOF
# Database Configuration
DATABASE_URL=${DATABASE_URL}
DATABASE_USER=${DATABASE_USER}
DATABASE_PASSWORD=${DATABASE_PASSWORD}

# AI Model API Keys
OPENAI_API_KEY=${OPENAI_API_KEY}
ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
GROQ_API_KEY=${GROQ_API_KEY}
GOOGLE_API_KEY=${GOOGLE_API_KEY}
MISTRAL_API_KEY=${MISTRAL_API_KEY}
DEEPSEEK_API_KEY=${DEEPSEEK_API_KEY}

# Ollama Configuration
OLLAMA_BASE_URL=${OLLAMA_BASE_URL}

# Application Settings
DEBUG=${DEBUG}
LOG_LEVEL=${LOG_LEVEL}
MAX_FILE_SIZE_MB=${MAX_FILE_SIZE}

# Security
ENABLE_AUTH=${ENABLE_AUTH}
AUTH_USERNAME=${AUTH_USERNAME}
AUTH_PASSWORD=${AUTH_PASSWORD}

# Paths
DATA_DIR=/config/open-notebook
SHARE_DIR=/share/open-notebook
EOF

# Log configuration
bashio::log.info "Open Notebook Configuration:"
bashio::log.info "- Database URL: ${DATABASE_URL}"
bashio::log.info "- Debug Mode: ${DEBUG}"
bashio::log.info "- Log Level: ${LOG_LEVEL}"
bashio::log.info "- Max File Size: ${MAX_FILE_SIZE}MB"
bashio::log.info "- Authentication: ${ENABLE_AUTH}"

# Check if at least one AI API key is configured
if [[ -n "${OPENAI_API_KEY}" ]]; then
    bashio::log.info "- OpenAI API: Configured"
elif [[ -n "${ANTHROPIC_API_KEY}" ]]; then
    bashio::log.info "- Anthropic API: Configured"
elif [[ -n "${GROQ_API_KEY}" ]]; then
    bashio::log.info "- Groq API: Configured"
elif [[ -n "${GOOGLE_API_KEY}" ]]; then
    bashio::log.info "- Google API: Configured"
elif [[ -n "${MISTRAL_API_KEY}" ]]; then
    bashio::log.info "- Mistral API: Configured"
elif [[ -n "${DEEPSEEK_API_KEY}" ]]; then
    bashio::log.info "- DeepSeek API: Configured"
elif [[ -n "${OLLAMA_BASE_URL}" ]]; then
    bashio::log.info "- Ollama: Configured at ${OLLAMA_BASE_URL}"
else
    bashio::log.warning "No AI API keys configured. Please add at least one API key in the addon configuration."
fi

# Set environment
export PYTHONPATH="/app"

# Change to app directory
cd /app

# Start Streamlit
bashio::log.info "Starting Streamlit on port 8501..."
exec streamlit run app_home.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true --server.enableCORS=false --server.enableXsrfProtection=false
