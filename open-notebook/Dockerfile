ARG BUILD_FROM
FROM $BUILD_FROM

# Install basic dependencies
RUN apk add --no-cache python3 py3-pip curl

# Set working directory
WORKDIR /app

# Install minimal Python packages
RUN pip3 install --no-cache-dir streamlit fastapi uvicorn python-dotenv loguru

# Copy only essential files
COPY app_home.py /app/
COPY run.sh /

# Create directories
RUN mkdir -p /app/logs /config/open-notebook /share/open-notebook

# Set permissions
RUN chmod +x /run.sh

# Expose port
EXPOSE 8501

# Simple health check
HEALTHCHECK --interval=60s --timeout=30s --start-period=120s --retries=2 \
    CMD curl -f http://localhost:8501 || exit 1

# Run
CMD ["/run.sh"]
