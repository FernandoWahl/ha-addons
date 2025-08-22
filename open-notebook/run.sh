#!/bin/bash

# ==============================================================================
# Home Assistant Add-on: Open Notebook - Full Version
# ==============================================================================

echo "=========================================="
echo "🚀 Starting Open Notebook v0.5.1 - ARM64 OPTIMIZED"
echo "⏰ $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="

# Step 1: Create directories
echo "📁 Creating directories..."
mkdir -p /config/open-notebook/{data,notebooks,uploads,exports}
mkdir -p /share/open-notebook/{documents,podcasts,models}
mkdir -p /app/{logs,data}
echo "✅ Directories created successfully"

# Step 2: Set permissions
echo "🔐 Setting permissions..."
chmod -R 755 /config/open-notebook
chmod -R 755 /share/open-notebook
chmod -R 755 /app/data
echo "✅ Permissions set successfully"

# Step 3: Read configuration from Home Assistant
echo "⚙️ Reading configuration from Home Assistant..."

# Function to read config with fallback
read_config() {
    local key="$1"
    local default="$2"
    
    if command -v bashio >/dev/null 2>&1; then
        bashio::config "$key" "$default" 2>/dev/null || echo "$default"
    else
        # Fallback: try to read from options.json
        if [ -f "/data/options.json" ]; then
            python3 -c "
import json, sys
try:
    with open('/data/options.json') as f:
        data = json.load(f)
    print(data.get('$key', '$default'))
except:
    print('$default')
" 2>/dev/null || echo "$default"
        else
            echo "$default"
        fi
    fi
}

DATABASE_URL=$(read_config 'database_url' 'file:///config/open-notebook/data/database.db')
DATABASE_USER=$(read_config 'database_user' 'root')
DATABASE_PASSWORD=$(read_config 'database_password' 'root')
DEBUG=$(read_config 'debug' 'false')
LOG_LEVEL=$(read_config 'log_level' 'INFO')
MAX_FILE_SIZE=$(read_config 'max_file_size' '50')
ENABLE_AUTH=$(read_config 'enable_auth' 'false')

# AI API Keys
OPENAI_API_KEY=$(read_config 'openai_api_key' '')
ANTHROPIC_API_KEY=$(read_config 'anthropic_api_key' '')
GROQ_API_KEY=$(read_config 'groq_api_key' '')
GOOGLE_API_KEY=$(read_config 'google_api_key' '')
MISTRAL_API_KEY=$(read_config 'mistral_api_key' '')
DEEPSEEK_API_KEY=$(read_config 'deepseek_api_key' '')
OLLAMA_BASE_URL=$(read_config 'ollama_base_url' '')

# Authentication
AUTH_USERNAME=$(read_config 'auth_username' '')
AUTH_PASSWORD=$(read_config 'auth_password' '')

echo "✅ Configuration loaded successfully"

# Step 4: Count configured providers
echo "🤖 Checking AI provider configurations..."
PROVIDER_COUNT=0

if [[ -n "${OPENAI_API_KEY}" ]]; then
    echo "  ✅ OpenAI API configured"
    PROVIDER_COUNT=$((PROVIDER_COUNT + 1))
fi
if [[ -n "${ANTHROPIC_API_KEY}" ]]; then
    echo "  ✅ Anthropic API configured"
    PROVIDER_COUNT=$((PROVIDER_COUNT + 1))
fi
if [[ -n "${GROQ_API_KEY}" ]]; then
    echo "  ✅ Groq API configured"
    PROVIDER_COUNT=$((PROVIDER_COUNT + 1))
fi
if [[ -n "${GOOGLE_API_KEY}" ]]; then
    echo "  ✅ Google AI API configured"
    PROVIDER_COUNT=$((PROVIDER_COUNT + 1))
fi
if [[ -n "${MISTRAL_API_KEY}" ]]; then
    echo "  ✅ Mistral AI API configured"
    PROVIDER_COUNT=$((PROVIDER_COUNT + 1))
fi
if [[ -n "${DEEPSEEK_API_KEY}" ]]; then
    echo "  ✅ DeepSeek API configured"
    PROVIDER_COUNT=$((PROVIDER_COUNT + 1))
fi
if [[ -n "${OLLAMA_BASE_URL}" ]]; then
    echo "  ✅ Ollama configured at: ${OLLAMA_BASE_URL}"
    PROVIDER_COUNT=$((PROVIDER_COUNT + 1))
fi

echo "🤖 Total AI providers configured: ${PROVIDER_COUNT}"

# Step 5: Create comprehensive environment file
echo "📝 Creating comprehensive environment configuration..."

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

echo "✅ Comprehensive environment file created"

# Step 6: Initialize database (optional)
echo "🗄️ Checking database initialization..."
cd /app
if [ -f "open_notebook/database/migrate.py" ]; then
    python3 -c "
import os, sys
sys.path.insert(0, '/app')
try:
    from open_notebook.database.migrate import run_migrations
    run_migrations()
    print('✅ Database initialized successfully')
except Exception as e:
    print(f'⚠️ Database initialization: {e}')
" 2>/dev/null || echo "⚠️ Database initialization skipped"
else
    echo "⚠️ Database migration not available"
fi

# Step 7: Configuration summary
echo "📊 Full Configuration Summary:"
echo "  🗄️ Database: ${DATABASE_URL}"
echo "  🐛 Debug: ${DEBUG}"
echo "  📝 Log Level: ${LOG_LEVEL}"
echo "  📁 Max File Size: ${MAX_FILE_SIZE}MB"
echo "  🔐 Authentication: ${ENABLE_AUTH}"
echo "  🤖 AI Providers: ${PROVIDER_COUNT} configured"
echo "  📄 Document Processing: Enabled"
echo "  🎙️ Podcast Processing: Enabled"
echo "  🔍 Search & Embeddings: Enabled"

# Step 8: Validate AI configuration
if [[ ${PROVIDER_COUNT} -eq 0 ]]; then
    echo "⚠️ WARNING: No AI providers configured!"
    echo "   Please configure at least one AI API key for full functionality"
    echo "   Add keys in: Supervisor → Add-on Store → Open Notebook → Configuration"
else
    echo "✅ AI configuration ready - ${PROVIDER_COUNT} provider(s) available"
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
echo "=========================================="
echo "🌟 Starting Open Notebook Full Services"
echo "⏰ $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="
echo "🌐 Streamlit Frontend: http://[HOST]:8501"
echo "⚡ FastAPI Backend: http://[HOST]:8000"
echo "🗄️ Database: ${DATABASE_URL}"
echo "📁 Data Directory: /config/open-notebook"
echo "📂 Shared Storage: /share/open-notebook"
echo "=========================================="

echo "🚀 Launching supervisor with full services..."

# Start supervisor to manage all services
exec supervisord -c /app/supervisord.conf
