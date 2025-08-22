#!/bin/bash

echo "🚀 Starting Open Notebook v0.4.2 (Minimal)"

# Create directories
mkdir -p /config/open-notebook /share/open-notebook /app/logs

# Create basic .env if config exists
if [ -f "/data/options.json" ]; then
    echo "📝 Loading configuration..."
    
    # Simple config parsing (basic)
    cat > /app/.env << 'EOF'
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GROQ_API_KEY=
DEBUG=false
EOF
    
    echo "✅ Configuration loaded"
fi

# Set environment
export PYTHONPATH="/app"
cd /app

echo "🌊 Starting Streamlit on port 8501..."

# Start Streamlit
exec streamlit run app_home.py \
    --server.port=8501 \
    --server.address=0.0.0.0 \
    --server.headless=true
