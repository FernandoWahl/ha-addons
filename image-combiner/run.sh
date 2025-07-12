#!/usr/bin/with-contenv bashio

# Get configuration from Home Assistant
MAX_IMAGES=$(bashio::config 'max_images')
IMAGE_QUALITY=$(bashio::config 'image_quality')
CELL_WIDTH=$(bashio::config 'cell_width')
CELL_HEIGHT=$(bashio::config 'cell_height')
TIMEOUT=$(bashio::config 'timeout')

# Export environment variables for the Python app
export MAX_IMAGES
export IMAGE_QUALITY
export CELL_WIDTH
export CELL_HEIGHT
export TIMEOUT

# Log configuration
bashio::log.info "Starting Image Combiner addon..."
bashio::log.info "Max images: ${MAX_IMAGES}"
bashio::log.info "Image quality: ${IMAGE_QUALITY}"
bashio::log.info "Cell dimensions: ${CELL_WIDTH}x${CELL_HEIGHT}"
bashio::log.info "Timeout: ${TIMEOUT}s"

# Start the Python application
cd /app
exec python3 app.py
