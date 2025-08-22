#!/usr/bin/with-contenv bashio

# ==============================================================================
# Home Assistant Add-on: Open Notebook - Full Application
# ==============================================================================

bashio::log.info "=========================================="
bashio::log.info "🚀 Starting Open Notebook v0.4.0 - Full Application"
bashio::log.info "=========================================="

# Step 1: Create directories
bashio::log.info "📁 Creating directories..."
mkdir -p /config/open-notebook
mkdir -p /share/open-notebook
mkdir -p /app/logs
mkdir -p /app/data
bashio::log.info "✅ Directories created successfully"

# Step 2: Set permissions
bashio::log.info "🔐 Setting permissions..."
chmod -R 755 /config/open-notebook
chmod -R 755 /share/open-notebook
bashio::log.info "✅ Permissions set successfully"

# Step 3: Read configuration
bashio::log.info "⚙️ Reading configuration from Home Assistant..."

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

bashio::log.info "✅ Configuration loaded successfully"

# Step 4: Count configured providers
PROVIDER_COUNT=0
if [[ -n "${OPENAI_API_KEY}" ]]; then
    bashio::log.info "  ✅ OpenAI API configured"
    PROVIDER_COUNT=$((PROVIDER_COUNT + 1))
fi
if [[ -n "${ANTHROPIC_API_KEY}" ]]; then
    bashio::log.info "  ✅ Anthropic API configured"
    PROVIDER_COUNT=$((PROVIDER_COUNT + 1))
fi
if [[ -n "${GROQ_API_KEY}" ]]; then
    bashio::log.info "  ✅ Groq API configured"
    PROVIDER_COUNT=$((PROVIDER_COUNT + 1))
fi
if [[ -n "${GOOGLE_API_KEY}" ]]; then
    bashio::log.info "  ✅ Google AI API configured"
    PROVIDER_COUNT=$((PROVIDER_COUNT + 1))
fi
if [[ -n "${MISTRAL_API_KEY}" ]]; then
    bashio::log.info "  ✅ Mistral AI API configured"
    PROVIDER_COUNT=$((PROVIDER_COUNT + 1))
fi
if [[ -n "${DEEPSEEK_API_KEY}" ]]; then
    bashio::log.info "  ✅ DeepSeek API configured"
    PROVIDER_COUNT=$((PROVIDER_COUNT + 1))
fi
if [[ -n "${OLLAMA_BASE_URL}" ]]; then
    bashio::log.info "  ✅ Ollama configured at: ${OLLAMA_BASE_URL}"
    PROVIDER_COUNT=$((PROVIDER_COUNT + 1))
fi

bashio::log.info "🤖 Total AI providers configured: ${PROVIDER_COUNT}"

# Step 5: Create environment file
bashio::log.info "📝 Creating environment configuration..."

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

bashio::log.info "✅ Environment file created"

# Step 6: Configuration summary
bashio::log.info "📊 Configuration Summary:"
bashio::log.info "  🗄️ Database: ${DATABASE_URL}"
bashio::log.info "  🐛 Debug: ${DEBUG}"
bashio::log.info "  📝 Log Level: ${LOG_LEVEL}"
bashio::log.info "  🤖 AI Providers: ${PROVIDER_COUNT} configured"

# Step 7: Validate AI configuration
if [[ ${PROVIDER_COUNT} -eq 0 ]]; then
    bashio::log.warning "⚠️ No AI providers configured - some features will be limited"
else
    bashio::log.info "✅ AI configuration ready"
fi

# Step 8: Set environment
export PYTHONPATH="/app"
export PYTHONUNBUFFERED=1

# Step 9: Change to app directory
cd /app

# Step 10: Start services with supervisor
bashio::log.info "=========================================="
bashio::log.info "🌟 Starting Open Notebook Services"
bashio::log.info "=========================================="
bashio::log.info "🌐 Streamlit UI: http://[HOST]:8501"
bashio::log.info "⚡ FastAPI Backend: http://[HOST]:8000"
bashio::log.info "=========================================="

# Start supervisor to manage both services
exec supervisord -c /app/supervisord.conf
