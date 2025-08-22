#!/usr/bin/with-contenv bashio

# ==============================================================================
# Home Assistant Add-on: Open Notebook
# Runs Open Notebook application
# ==============================================================================

# Set up configuration
CONFIG_PATH="/data/options.json"

# Read configuration
DATABASE_URL=$(bashio::config 'database_url')
DATABASE_USER=$(bashio::config 'database_user')
DATABASE_PASSWORD=$(bashio::config 'database_password')
OPENAI_API_KEY=$(bashio::config 'openai_api_key')
ANTHROPIC_API_KEY=$(bashio::config 'anthropic_api_key')
GROQ_API_KEY=$(bashio::config 'groq_api_key')
GOOGLE_API_KEY=$(bashio::config 'google_api_key')
MISTRAL_API_KEY=$(bashio::config 'mistral_api_key')
DEEPSEEK_API_KEY=$(bashio::config 'deepseek_api_key')
OLLAMA_BASE_URL=$(bashio::config 'ollama_base_url')
DEBUG=$(bashio::config 'debug')
LOG_LEVEL=$(bashio::config 'log_level')
MAX_FILE_SIZE=$(bashio::config 'max_file_size')
ENABLE_AUTH=$(bashio::config 'enable_auth')
AUTH_USERNAME=$(bashio::config 'auth_username')
AUTH_PASSWORD=$(bashio::config 'auth_password')

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

# Create data directories
mkdir -p /config/open-notebook
mkdir -p /share/open-notebook
mkdir -p /app/data
mkdir -p /app/logs

# Set permissions
chown -R root:root /config/open-notebook
chown -R root:root /share/open-notebook
chmod -R 755 /config/open-notebook
chmod -R 755 /share/open-notebook

# Log startup
bashio::log.info "Starting Open Notebook..."
bashio::log.info "Database URL: ${DATABASE_URL}"
bashio::log.info "Debug mode: ${DEBUG}"
bashio::log.info "Log level: ${LOG_LEVEL}"

# Change to app directory
cd /app

# Start supervisor to manage both services
exec supervisord -c /app/supervisord.conf
