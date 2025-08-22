ARG BUILD_FROM
FROM $BUILD_FROM

# Minimal installation
RUN apk add --no-cache python3 py3-pip curl
RUN pip3 install --no-cache-dir streamlit python-dotenv

# Set working directory
WORKDIR /app

# Copy minimal files
COPY app_home_minimal.py /app/app_home.py
COPY run_minimal.sh /run.sh

# Create directories and set permissions
RUN mkdir -p /app/logs /config/open-notebook /share/open-notebook && \
    chmod +x /run.sh

# Expose port
EXPOSE 8501

# Simple health check
HEALTHCHECK --interval=60s --timeout=10s --start-period=30s --retries=2 \
    CMD curl -f http://localhost:8501 || exit 1

# Run
CMD ["/run.sh"]
