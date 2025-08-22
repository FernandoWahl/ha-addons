#!/usr/bin/with-contenv bashio

# ==============================================================================
# Home Assistant Add-on: Open Notebook
# Detailed startup logging
# ==============================================================================

bashio::log.info "=========================================="
bashio::log.info "🚀 Starting Open Notebook v0.3.4"
bashio::log.info "=========================================="

# Step 1: Create directories
bashio::log.info "📁 Creating directories..."
mkdir -p /config/open-notebook
mkdir -p /share/open-notebook
mkdir -p /app/logs
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

bashio::log.info "✅ Basic configuration loaded"

# Step 4: Read AI API Keys
bashio::log.info "🤖 Loading AI provider configurations..."

OPENAI_API_KEY=$(bashio::config 'openai_api_key' '')
ANTHROPIC_API_KEY=$(bashio::config 'anthropic_api_key' '')
GROQ_API_KEY=$(bashio::config 'groq_api_key' '')
GOOGLE_API_KEY=$(bashio::config 'google_api_key' '')
MISTRAL_API_KEY=$(bashio::config 'mistral_api_key' '')
DEEPSEEK_API_KEY=$(bashio::config 'deepseek_api_key' '')
OLLAMA_BASE_URL=$(bashio::config 'ollama_base_url' '')

# Count configured providers
PROVIDER_COUNT=0
if [[ -n "${OPENAI_API_KEY}" ]]; then
    bashio::log.info "  ✅ OpenAI API key configured"
    PROVIDER_COUNT=$((PROVIDER_COUNT + 1))
fi

if [[ -n "${ANTHROPIC_API_KEY}" ]]; then
    bashio::log.info "  ✅ Anthropic API key configured"
    PROVIDER_COUNT=$((PROVIDER_COUNT + 1))
fi

if [[ -n "${GROQ_API_KEY}" ]]; then
    bashio::log.info "  ✅ Groq API key configured"
    PROVIDER_COUNT=$((PROVIDER_COUNT + 1))
fi

if [[ -n "${GOOGLE_API_KEY}" ]]; then
    bashio::log.info "  ✅ Google AI API key configured"
    PROVIDER_COUNT=$((PROVIDER_COUNT + 1))
fi

if [[ -n "${MISTRAL_API_KEY}" ]]; then
    bashio::log.info "  ✅ Mistral AI API key configured"
    PROVIDER_COUNT=$((PROVIDER_COUNT + 1))
fi

if [[ -n "${DEEPSEEK_API_KEY}" ]]; then
    bashio::log.info "  ✅ DeepSeek API key configured"
    PROVIDER_COUNT=$((PROVIDER_COUNT + 1))
fi

if [[ -n "${OLLAMA_BASE_URL}" ]]; then
    bashio::log.info "  ✅ Ollama configured at: ${OLLAMA_BASE_URL}"
    PROVIDER_COUNT=$((PROVIDER_COUNT + 1))
fi

bashio::log.info "🤖 Total AI providers configured: ${PROVIDER_COUNT}"

# Step 5: Read Authentication
AUTH_USERNAME=$(bashio::config 'auth_username' '')
AUTH_PASSWORD=$(bashio::config 'auth_password' '')

if [[ "${ENABLE_AUTH}" == "true" ]]; then
    if [[ -n "${AUTH_USERNAME}" && -n "${AUTH_PASSWORD}" ]]; then
        bashio::log.info "🔐 Authentication enabled with username: ${AUTH_USERNAME}"
    else
        bashio::log.warning "⚠️ Authentication enabled but username/password not configured!"
    fi
else
    bashio::log.info "🔓 Authentication disabled"
fi

# Step 6: Create environment file
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

bashio::log.info "✅ Environment file created at /app/.env"

# Step 7: Display configuration summary
bashio::log.info "📊 Configuration Summary:"
bashio::log.info "  🗄️ Database: ${DATABASE_URL}"
bashio::log.info "  🐛 Debug Mode: ${DEBUG}"
bashio::log.info "  📝 Log Level: ${LOG_LEVEL}"
bashio::log.info "  📁 Max File Size: ${MAX_FILE_SIZE}MB"
bashio::log.info "  🔐 Authentication: ${ENABLE_AUTH}"
bashio::log.info "  🤖 AI Providers: ${PROVIDER_COUNT} configured"

# Step 8: Validate configuration
if [[ ${PROVIDER_COUNT} -eq 0 ]]; then
    bashio::log.warning "⚠️ WARNING: No AI providers configured!"
    bashio::log.warning "   Please configure at least one AI API key in the addon settings."
    bashio::log.warning "   The application will start but AI features will not work."
else
    bashio::log.info "✅ AI configuration validated - ${PROVIDER_COUNT} provider(s) ready"
fi

# Step 9: Set Python environment
bashio::log.info "🐍 Setting up Python environment..."
export PYTHONPATH="/app"
export PYTHONUNBUFFERED=1
bashio::log.info "✅ Python environment configured"

# Step 10: Change to app directory
bashio::log.info "📂 Changing to application directory..."
cd /app
bashio::log.info "✅ Working directory: $(pwd)"

# Step 11: Test Streamlit installation
bashio::log.info "🧪 Testing Streamlit installation..."
if command -v streamlit >/dev/null 2>&1; then
    STREAMLIT_VERSION=$(streamlit version 2>/dev/null | head -n1 || echo "Unknown")
    bashio::log.info "✅ Streamlit available: ${STREAMLIT_VERSION}"
else
    bashio::log.error "❌ Streamlit not found!"
    exit 1
fi

# Step 12: Check application file
bashio::log.info "📄 Checking application file..."
if [[ -f "/app/app_home.py" ]]; then
    bashio::log.info "✅ Application file found: app_home.py"
else
    bashio::log.error "❌ Application file not found: app_home.py"
    exit 1
fi

# Step 13: Start Streamlit
bashio::log.info "=========================================="
bashio::log.info "🌟 Starting Streamlit Web Interface"
bashio::log.info "=========================================="
bashio::log.info "🌐 Server will be available at:"
bashio::log.info "   - Internal: http://localhost:8501"
bashio::log.info "   - External: http://[HOST]:8501"
bashio::log.info "=========================================="

# Add startup delay to ensure everything is ready
sleep 2

bashio::log.info "🚀 Launching Streamlit application..."

# Start Streamlit with detailed logging
exec streamlit run app_home.py \
    --server.port=8501 \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false \
    --logger.level=${LOG_LEVEL}
