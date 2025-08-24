#!/bin/bash

# ==============================================================================
# Home Assistant Add-on: Open Notebook
# Pure interface to original Open Notebook with PostgreSQL support
# ==============================================================================

echo "🚀 Open Notebook Interface v3.0.0"
echo "⏰ $(date '+%Y-%m-%d %H:%M:%S')"
echo "🗄️ PostgreSQL Compatible Version"
echo "=========================================="

# Function to read Home Assistant configuration
read_config() {
    local key="$1"
    local default="$2"
    local value=""
    
    # Try bashio first
    if command -v bashio >/dev/null 2>&1; then
        value=$(bashio::config "$key" "$default" 2>/dev/null)
        if [[ -n "$value" && "$value" != "$default" ]]; then
            echo "$value"
            return
        fi
    fi
    
    # Fallback: try to read from options.json
    if [ -f "/data/options.json" ]; then
        value=$(python3 -c "
import json, sys
try:
    with open('/data/options.json') as f:
        data = json.load(f)
    result = data.get('$key', '$default')
    if result and result != '$default':
        print(result)
    else:
        print('$default')
except Exception as e:
    print('$default')
" 2>/dev/null)
        
        if [[ -n "$value" ]]; then
            echo "$value"
            return
        fi
    fi
    
    # Final fallback
    echo "$default"
}

# Read database configuration
echo "⚙️ Reading database configuration..."

DATABASE_TYPE=$(read_config 'database_type' 'postgresql')
POSTGRES_HOST=$(read_config 'postgres_host' '')
POSTGRES_PORT=$(read_config 'postgres_port' '5432')
POSTGRES_DATABASE=$(read_config 'postgres_database' 'open_notebook')
POSTGRES_USER=$(read_config 'postgres_user' '')
POSTGRES_PASSWORD=$(read_config 'postgres_password' '')

# Read application configuration
echo "⚙️ Reading application configuration..."

OPENAI_API_KEY=$(read_config 'openai_api_key' '')
ANTHROPIC_API_KEY=$(read_config 'anthropic_api_key' '')
GROQ_API_KEY=$(read_config 'groq_api_key' '')
GOOGLE_API_KEY=$(read_config 'google_api_key' '')
MISTRAL_API_KEY=$(read_config 'mistral_api_key' '')
DEEPSEEK_API_KEY=$(read_config 'deepseek_api_key' '')
OLLAMA_BASE_URL=$(read_config 'ollama_base_url' '')

DEBUG=$(read_config 'debug' 'false')
LOG_LEVEL=$(read_config 'log_level' 'INFO')
MAX_FILE_SIZE=$(read_config 'max_file_size' '50')

ENABLE_AUTH=$(read_config 'enable_auth' 'false')
AUTH_USERNAME=$(read_config 'auth_username' '')
AUTH_PASSWORD=$(read_config 'auth_password' '')

# Configure database URL
if [[ "$DATABASE_TYPE" == "postgresql" ]]; then
    if [[ -z "$POSTGRES_HOST" || -z "$POSTGRES_USER" || -z "$POSTGRES_PASSWORD" ]]; then
        echo "❌ PostgreSQL configuration incomplete!"
        echo "   Please configure: postgres_host, postgres_user, postgres_password"
        echo "   Falling back to SQLite..."
        DATABASE_URL="sqlite:///data/open_notebook.db"
        echo "📁 Using SQLite: /data/open_notebook.db"
    else
        DATABASE_URL="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DATABASE}"
        echo "🐘 Using PostgreSQL: ${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DATABASE}"
        
        # Test PostgreSQL connection
        echo "🔍 Testing PostgreSQL connection..."
        python3 -c "
import psycopg2
try:
    conn = psycopg2.connect(
        host='${POSTGRES_HOST}',
        port=${POSTGRES_PORT},
        database='${POSTGRES_DATABASE}',
        user='${POSTGRES_USER}',
        password='${POSTGRES_PASSWORD}'
    )
    conn.close()
    print('✅ PostgreSQL connection successful')
except Exception as e:
    print(f'❌ PostgreSQL connection failed: {e}')
    print('   Falling back to SQLite...')
    exit(1)
" || {
            echo "🔄 Falling back to SQLite due to connection failure"
            DATABASE_URL="sqlite:///data/open_notebook.db"
        }
    fi
else
    DATABASE_URL="sqlite:///data/open_notebook.db"
    echo "📁 Using SQLite: /data/open_notebook.db"
fi

# Create .env file for Open Notebook
echo "📝 Creating configuration file..."

cd /app/open-notebook-src

cat > .env << EOF
# Database Configuration
DATABASE_URL=${DATABASE_URL}

# SurrealDB Configuration (disabled - using PostgreSQL)
SURREALDB_URL=disabled
SURREALDB_USER=root
SURREALDB_PASSWORD=root
SURREALDB_NAMESPACE=open_notebook
SURREALDB_DATABASE=main
USE_SURREALDB=false
SKIP_SURREALDB_MIGRATION=true

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
DATA_PATH=/data
LOGS_PATH=/app/logs

# Force PostgreSQL/SQLite usage
USE_POSTGRESQL=true
DISABLE_SURREALDB=true
EOF

echo "✅ Configuration created successfully"

# Apply patches to disable SurrealDB migrations
echo "🔧 Applying PostgreSQL compatibility patches..."
python3 /app/patch_migrations.py

# Show configuration summary (without sensitive data)
echo "📊 Configuration Summary:"
echo "  🗄️ Database: $(echo $DATABASE_URL | sed 's/:\/\/.*@/:\/\/***@/')"
echo "  🤖 OpenAI: $([ -n "$OPENAI_API_KEY" ] && echo "✅ Configured" || echo "❌ Not set")"
echo "  🤖 Anthropic: $([ -n "$ANTHROPIC_API_KEY" ] && echo "✅ Configured" || echo "❌ Not set")"
echo "  🤖 Groq: $([ -n "$GROQ_API_KEY" ] && echo "✅ Configured" || echo "❌ Not set")"
echo "  🤖 Google: $([ -n "$GOOGLE_API_KEY" ] && echo "✅ Configured" || echo "❌ Not set")"
echo "  🤖 Ollama: $([ -n "$OLLAMA_BASE_URL" ] && echo "✅ $OLLAMA_BASE_URL" || echo "❌ Not set")"
echo "  🔒 Auth: $([ "$ENABLE_AUTH" == "true" ] && echo "✅ Enabled" || echo "❌ Disabled")"
echo "  🐛 Debug: $DEBUG"

# Ensure data directory exists
mkdir -p /data /app/logs

# Start services with supervisor
echo "=========================================="
echo "🚀 Starting Open Notebook services..."
echo "🌐 Streamlit UI: http://[HOST]:8501"
echo "🔌 FastAPI: http://[HOST]:8000"
echo "=========================================="

exec /usr/bin/supervisord -c /app/supervisord.conf
