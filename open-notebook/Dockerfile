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
    && pip3 install --no-cache-dir --upgrade pip

# Set working directory
WORKDIR /app

# Copy requirements and install Python packages
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# Copy essential application files
COPY app_home_working.py /app/app_home.py
COPY run_api.py /app/
COPY run.sh /
COPY supervisord.conf /app/

# Create directories
RUN mkdir -p /app/logs /app/data /config/open-notebook /share/open-notebook

# Set permissions
RUN chmod +x /run.sh

# Expose ports
EXPOSE 8501 8000

# Health check
HEALTHCHECK --interval=60s --timeout=30s --start-period=180s --retries=3 \
    CMD curl -f http://localhost:8501 || exit 1

# Run
CMD ["/run.sh"]
