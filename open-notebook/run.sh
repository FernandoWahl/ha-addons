#!/usr/bin/with-contenv bashio
set -e

# Display startup banner
echo "🚀 Open Notebook Interface v3.2.3"
echo "⏰ $(date)"
echo "🗄️ PostgreSQL Compatible Version with SIGILL Protection"
echo "=========================================="

# Read configuration
echo "⚙️ Reading database configuration..."
DB_HOST=$(bashio::services "postgres" "host")
DB_PORT=$(bashio::services "postgres" "port")
DB_USERNAME=$(bashio::services "postgres" "username")
DB_PASSWORD=$(bashio::services "postgres" "password")
DB_DATABASE="open_notebook"

echo "⚙️ Reading application configuration..."
OPENAI_API_KEY=$(bashio::config 'openai_api_key' '')
ANTHROPIC_API_KEY=$(bashio::config 'anthropic_api_key' '')
GROQ_API_KEY=$(bashio::config 'groq_api_key' '')
GOOGLE_API_KEY=$(bashio::config 'google_api_key' '')
OLLAMA_BASE_URL=$(bashio::config 'ollama_base_url' '')
AUTH_ENABLED=$(bashio::config 'auth_enabled' 'false')
DEBUG_MODE=$(bashio::config 'debug_mode' 'true')

# Construct PostgreSQL connection string
POSTGRES_URL="postgresql://${DB_USERNAME}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_DATABASE}"
echo "🐘 Using PostgreSQL: ${DB_HOST}:${DB_PORT}/${DB_DATABASE}"

# Test PostgreSQL connection
echo "🔍 Testing PostgreSQL connection..."
if python3 -c "
import psycopg2
try:
    conn = psycopg2.connect('${POSTGRES_URL}')
    conn.close()
    print('✅ PostgreSQL connection successful')
except Exception as e:
    print(f'❌ PostgreSQL connection failed: {e}')
    exit(1)
"; then
    echo "✅ PostgreSQL connection successful"
else
    echo "❌ PostgreSQL connection failed"
    exit 1
fi

# Create configuration file
echo "📝 Creating configuration file..."
cd /app/open-notebook-src

cat > .env << EOF
# Database Configuration
DATABASE_URL=${POSTGRES_URL}
USE_POSTGRESQL=true
SKIP_SURREALDB_MIGRATION=true

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
HOST=0.0.0.0
PORT=8000
API_BASE_URL=http://localhost:8000

# AI Service Configuration
OPENAI_API_KEY=${OPENAI_API_KEY}
ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
GROQ_API_KEY=${GROQ_API_KEY}
GOOGLE_API_KEY=${GOOGLE_API_KEY}
OLLAMA_BASE_URL=${OLLAMA_BASE_URL}

# Application Configuration
AUTH_ENABLED=${AUTH_ENABLED}
DEBUG=${DEBUG_MODE}

# Streamlit Safety Configuration
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_SERVER_ENABLE_CORS=false
STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
STREAMLIT_SERVER_RUN_ON_SAVE=false
STREAMLIT_SERVER_ENABLE_WEBSOCKET_COMPRESSION=false
STREAMLIT_GLOBAL_DEVELOPMENT_MODE=false
PYTHONOPTIMIZE=1
PYTHONDONTWRITEBYTECODE=1
EOF

echo "✅ Configuration created successfully"

# Run PostgreSQL compatibility setup
echo "🔧 Running PostgreSQL compatibility setup..."
python3 /app/pre_start.sh
echo "✅ PostgreSQL compatibility setup completed"

# Copy safe execution scripts
echo "📦 Installing SIGILL protection scripts..."
cp /app/streamlit_safe.py /app/open-notebook-src/
cp /app/fallback_server.py /app/open-notebook-src/
echo "✅ Protection scripts installed"

# Set environment variables
export USE_POSTGRESQL=true
export SKIP_SURREALDB_MIGRATION=true
export DATABASE_URL="${POSTGRES_URL}"
export API_PORT=8000
export HOST=0.0.0.0
export PORT=8000
export API_BASE_URL=http://localhost:8000
export PYTHONPATH=/app/open-notebook-src

# Safety environment variables
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_SERVER_ENABLE_CORS=false
export STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
export STREAMLIT_SERVER_RUN_ON_SAVE=false
export STREAMLIT_SERVER_ENABLE_WEBSOCKET_COMPRESSION=false
export STREAMLIT_GLOBAL_DEVELOPMENT_MODE=false
export PYTHONOPTIMIZE=1
export PYTHONDONTWRITEBYTECODE=1

echo "🐍 Environment configured for PostgreSQL"
echo "🗄️ Database mode: PostgreSQL"

# Display configuration summary
echo "📊 Configuration Summary:"
echo "  🗄️ Database: postgresql://***@${DB_HOST}:${DB_PORT}/${DB_DATABASE}"
echo "  🤖 OpenAI: $([ -n "$OPENAI_API_KEY" ] && echo "✅ Configured" || echo "❌ Not set")"
echo "  🤖 Anthropic: $([ -n "$ANTHROPIC_API_KEY" ] && echo "✅ Configured" || echo "❌ Not set")"
echo "  🤖 Groq: $([ -n "$GROQ_API_KEY" ] && echo "✅ Configured" || echo "❌ Not set")"
echo "  🤖 Google: $([ -n "$GOOGLE_API_KEY" ] && echo "✅ Configured" || echo "❌ Not set")"
echo "  🤖 Ollama: $([ -n "$OLLAMA_BASE_URL" ] && echo "✅ Configured" || echo "❌ Not set")"
echo "  🔒 Auth: $([ "$AUTH_ENABLED" = "true" ] && echo "✅ Enabled" || echo "❌ Disabled")"
echo "  🐛 Debug: $DEBUG_MODE"
echo "  🛡️ SIGILL Protection: ✅ Enabled"
echo "=========================================="

echo "🚀 Starting Open Notebook services..."
echo "🌐 Streamlit UI: http://[HOST]:8502"
echo "🔌 FastAPI: http://[HOST]:8000"
echo "🛡️ Fallback UI: Available if Streamlit fails"
echo "=========================================="

# Use updated supervisord configuration with SIGILL protection
exec /usr/bin/supervisord -c /app/supervisord_safe.conf
