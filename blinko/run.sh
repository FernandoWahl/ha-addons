#!/usr/bin/with-contenv bashio

# Get configuration
DATABASE_URL=$(bashio::config 'database_url')
OPENAI_API_KEY=$(bashio::config 'openai_api_key')
ANTHROPIC_API_KEY=$(bashio::config 'anthropic_api_key')
GROQ_API_KEY=$(bashio::config 'groq_api_key')
DEBUG=$(bashio::config 'debug')
LOG_LEVEL=$(bashio::config 'log_level')

# Set environment variables with memory optimization
export DATABASE_URL="$DATABASE_URL"
export OPENAI_API_KEY="$OPENAI_API_KEY"
export ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY"
export GROQ_API_KEY="$GROQ_API_KEY"
export DEBUG="$DEBUG"
export LOG_LEVEL="$LOG_LEVEL"
export NODE_ENV=production
export NODE_OPTIONS="--max-old-space-size=1024"

bashio::log.info "Starting Blinko add-on..."

# Clone or update Blinko repository
if [ ! -d "/app/blinko" ]; then
    bashio::log.info "Cloning Blinko repository..."
    git clone https://github.com/blinko-space/blinko.git /app/blinko
else
    bashio::log.info "Updating Blinko repository..."
    cd /app/blinko
    git pull origin main
fi

cd /app/blinko

# Install dependencies
bashio::log.info "Installing dependencies..."
bun install

# Generate Prisma client
bashio::log.info "Generating Prisma client..."
bun run prisma:generate

# Reset database if P3005 error occurs
bashio::log.info "Resetting database to avoid P3005 error..."
cd prisma && npx prisma migrate reset --force --skip-seed || true

# Run database migrations
bashio::log.info "Running database migrations..."
bun run prisma:migrate:deploy

# Build with memory optimization
bashio::log.info "Building Blinko with memory optimization..."
NODE_OPTIONS="--max-old-space-size=1024" bun run build:web

# Start the application
bashio::log.info "Starting Blinko server..."
exec bun run start
