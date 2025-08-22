#!/usr/bin/with-contenv bashio

# ==============================================================================
# Home Assistant Add-on: Open Notebook - Full Version
# ==============================================================================

bashio::log.info "=========================================="
bashio::log.info "🚀 Starting Open Notebook v0.5.0 - FULL VERSION"
bashio::log.info "=========================================="

# Step 1: Create directories
bashio::log.info "📁 Creating directories..."
mkdir -p /config/open-notebook/{data,notebooks,uploads,exports}
mkdir -p /share/open-notebook/{documents,podcasts,models}
mkdir -p /app/{logs,data}
bashio::log.info "✅ Directories created successfully"

# Step 2: Set permissions
bashio::log.info "🔐 Setting permissions..."
chmod -R 755 /config/open-notebook
chmod -R 755 /share/open-notebook
chmod -R 755 /app/data
bashio::log.info "✅ Permissions set successfully"

# Step 3: Read configuration
bashio::log.info "⚙️ Reading configuration from Home Assistant..."

DATABASE_URL=$(bashio::config 'database_url' 'file:///config/open-notebook/data/database.db')
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

# Step 5: Create comprehensive environment file
bashio::log.info "📝 Creating comprehensive environment configuration..."

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
DATA_DIR=/config/open-notebook/data
SHARE_DIR=/share/open-notebook
NOTEBOOKS_DIR=/config/open-notebook/notebooks
UPLOADS_DIR=/config/open-notebook/uploads
EXPORTS_DIR=/config/open-notebook/exports
DOCUMENTS_DIR=/share/open-notebook/documents
PODCASTS_DIR=/share/open-notebook/podcasts
MODELS_DIR=/share/open-notebook/models

# Application Configuration
STREAMLIT_SERVER_PORT=8501
FASTAPI_SERVER_PORT=8000
STREAMLIT_SERVER_ADDRESS=0.0.0.0
FASTAPI_SERVER_ADDRESS=0.0.0.0

# Feature Flags
ENABLE_DOCUMENT_PROCESSING=true
ENABLE_PODCAST_PROCESSING=true
ENABLE_EMBEDDINGS=true
ENABLE_SEARCH=true
ENABLE_TRANSFORMATIONS=true
EOF

bashio::log.info "✅ Comprehensive environment file created"

# Step 6: Initialize database
bashio::log.info "🗄️ Initializing database..."
cd /app
python3 -c "
import os
from open_notebook.database.migrate import run_migrations
try:
    run_migrations()
    print('✅ Database initialized successfully')
except Exception as e:
    print(f'⚠️ Database initialization: {e}')
" || bashio::log.warning "Database initialization skipped"

# Step 7: Configuration summary
bashio::log.info "📊 Full Configuration Summary:"
bashio::log.info "  🗄️ Database: ${DATABASE_URL}"
bashio::log.info "  🐛 Debug: ${DEBUG}"
bashio::log.info "  📝 Log Level: ${LOG_LEVEL}"
bashio::log.info "  📁 Max File Size: ${MAX_FILE_SIZE}MB"
bashio::log.info "  🔐 Authentication: ${ENABLE_AUTH}"
bashio::log.info "  🤖 AI Providers: ${PROVIDER_COUNT} configured"
bashio::log.info "  📄 Document Processing: Enabled"
bashio::log.info "  🎙️ Podcast Processing: Enabled"
bashio::log.info "  🔍 Search & Embeddings: Enabled"

# Step 8: Validate AI configuration
if [[ ${PROVIDER_COUNT} -eq 0 ]]; then
    bashio::log.warning "⚠️ No AI providers configured - AI features will be limited"
    bashio::log.warning "   Please configure at least one AI API key for full functionality"
else
    bashio::log.info "✅ AI configuration ready - ${PROVIDER_COUNT} provider(s) available"
fi

# Step 9: Set comprehensive environment
export PYTHONPATH="/app"
export PYTHONUNBUFFERED=1
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_SERVER_ENABLE_CORS=false
export STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false

# Step 10: Change to app directory
cd /app

# Step 11: Start comprehensive services
bashio::log.info "=========================================="
bashio::log.info "🌟 Starting Open Notebook Full Services"
bashio::log.info "=========================================="
bashio::log.info "🌐 Streamlit Frontend: http://[HOST]:8501"
bashio::log.info "⚡ FastAPI Backend: http://[HOST]:8000"
bashio::log.info "🗄️ Database: ${DATABASE_URL}"
bashio::log.info "📁 Data Directory: /config/open-notebook"
bashio::log.info "📂 Shared Storage: /share/open-notebook"
bashio::log.info "=========================================="

bashio::log.info "🚀 Launching supervisor with full services..."

# Start supervisor to manage all services
exec supervisord -c /app/supervisord.conf
