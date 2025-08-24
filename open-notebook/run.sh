#!/usr/bin/with-contenv bashio
set -e

# Display startup banner
echo "🚀 Open Notebook Interface v3.4.0"
echo "⏰ $(date)"
echo "🗄️ PostgreSQL Compatible - STABLE INTERFACE ONLY"
echo "=========================================="

# Read configuration - always use manual configuration from addon options
echo "⚙️ Reading database configuration..."
DB_HOST=$(bashio::config 'postgres_host' '')
DB_PORT=$(bashio::config 'postgres_port' '5432')
DB_USERNAME=$(bashio::config 'postgres_user' '')
DB_PASSWORD=$(bashio::config 'postgres_password' '')
DB_DATABASE=$(bashio::config 'postgres_database' 'open_notebook')

echo "⚙️ Reading application configuration..."
OPENAI_API_KEY=$(bashio::config 'openai_api_key' '')
ANTHROPIC_API_KEY=$(bashio::config 'anthropic_api_key' '')
GROQ_API_KEY=$(bashio::config 'groq_api_key' '')
GOOGLE_API_KEY=$(bashio::config 'google_api_key' '')
OLLAMA_BASE_URL=$(bashio::config 'ollama_base_url' '')
AUTH_ENABLED=$(bashio::config 'enable_auth' 'false')
DEBUG_MODE=$(bashio::config 'debug' 'true')

# Validate PostgreSQL configuration
if [ -z "$DB_HOST" ] || [ -z "$DB_USERNAME" ] || [ -z "$DB_PASSWORD" ]; then
    echo "❌ PostgreSQL configuration incomplete!"
    echo "   Host: '$DB_HOST'"
    echo "   Port: '$DB_PORT'"
    echo "   Username: '$DB_USERNAME'"
    echo "   Password: $([ -n "$DB_PASSWORD" ] && echo "***" || echo "NOT SET")"
    echo "   Database: '$DB_DATABASE'"
    exit 1
fi

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
EOF

echo "✅ Configuration created successfully"

# Run PostgreSQL compatibility setup
echo "🔧 Running PostgreSQL compatibility setup..."
bash /app/pre_start.sh
echo "✅ PostgreSQL compatibility setup completed"

# Set environment variables
export USE_POSTGRESQL=true
export SKIP_SURREALDB_MIGRATION=true
export DATABASE_URL="${POSTGRES_URL}"
export API_PORT=8000
export HOST=0.0.0.0
export PORT=8000
export API_BASE_URL=http://localhost:8000
export PYTHONPATH=/app/open-notebook-src

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
echo "=========================================="

echo "🚀 Starting Open Notebook services..."
echo "🌐 STABLE Interface: http://[HOST]:8502"
echo "🔌 FastAPI: http://[HOST]:8000"
echo "🚫 Streamlit: DISABLED (prevents SIGILL crashes)"
echo "=========================================="

# Start ONLY the API and Stable Interface - NO STREAMLIT EVER
exec /usr/bin/supervisord -c /app/supervisord.conf
