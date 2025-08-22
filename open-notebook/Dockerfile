ARG BUILD_FROM
FROM $BUILD_FROM

# Install system dependencies
RUN apk add --no-cache \
    python3 \
    py3-pip \
    curl \
    supervisor \
    build-base \
    python3-dev \
    libffi-dev \
    openssl-dev \
    sqlite \
    sqlite-dev \
    jpeg-dev \
    zlib-dev \
    freetype-dev \
    git \
    && pip3 install --no-cache-dir --upgrade pip uv

# Set working directory
WORKDIR /app

# Clone the original Open Notebook repository
RUN git clone https://github.com/lfnovo/open-notebook.git open-notebook-src

# Install Open Notebook using uv (faster than pip)
WORKDIR /app/open-notebook-src
RUN uv pip install --system -e .

# Go back to app directory
WORKDIR /app

# Copy only our interface files (no modifications to Open Notebook)
COPY run.sh /
COPY supervisord_interface.conf /app/supervisord.conf

# Create directories for Home Assistant integration
RUN mkdir -p /app/logs /config/open-notebook /share/open-notebook

# Set permissions
RUN chmod +x /run.sh

# Expose ports
EXPOSE 8501 8000

# Health check
HEALTHCHECK --interval=60s --timeout=30s --start-period=300s --retries=3 \
    CMD curl -f http://localhost:8501 || exit 1

# Run our interface script
CMD ["/run.sh"]
