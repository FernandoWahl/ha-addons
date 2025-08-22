#!/bin/bash

echo "Starting Open Notebook..."

# Create directories
mkdir -p /config/open-notebook
mkdir -p /share/open-notebook
mkdir -p /app/logs

# Create basic environment
export PYTHONPATH="/app"

# Change to app directory
cd /app

# Start Streamlit
echo "Starting Streamlit on port 8501..."
exec streamlit run app_home.py --server.port=8501 --server.address=0.0.0.0 --server.headless=true
