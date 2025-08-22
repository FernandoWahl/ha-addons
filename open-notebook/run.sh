#!/usr/bin/with-contenv bashio

# ==============================================================================
# Home Assistant Add-on: Open Notebook
# Runs Open Notebook application
# ==============================================================================

bashio::log.info "Starting Open Notebook..."

# Create data directories
mkdir -p /config/open-notebook
mkdir -p /share/open-notebook
mkdir -p /app/data
mkdir -p /app/logs

# Set permissions
chmod -R 755 /config/open-notebook
chmod -R 755 /share/open-notebook

# Create basic environment file
cat > /app/.env << EOF
# Basic configuration
DATABASE_URL=memory
DATABASE_USER=root
DATABASE_PASSWORD=root
DEBUG=false
LOG_LEVEL=INFO
DATA_DIR=/config/open-notebook
SHARE_DIR=/share/open-notebook
EOF

# Read configuration if available
if bashio::config.exists 'openai_api_key'; then
    OPENAI_API_KEY=$(bashio::config 'openai_api_key')
    echo "OPENAI_API_KEY=${OPENAI_API_KEY}" >> /app/.env
fi

if bashio::config.exists 'anthropic_api_key'; then
    ANTHROPIC_API_KEY=$(bashio::config 'anthropic_api_key')
    echo "ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}" >> /app/.env
fi

if bashio::config.exists 'groq_api_key'; then
    GROQ_API_KEY=$(bashio::config 'groq_api_key')
    echo "GROQ_API_KEY=${GROQ_API_KEY}" >> /app/.env
fi

bashio::log.info "Configuration loaded, starting services..."

# Change to app directory
cd /app

# Start supervisor to manage both services
exec supervisord -c /app/supervisord.conf
