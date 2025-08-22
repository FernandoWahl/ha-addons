ARG BUILD_FROM
FROM $BUILD_FROM

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Install system dependencies
RUN \
    apk add --no-cache \
        python3 \
        py3-pip \
        git \
        curl \
        supervisor \
        nodejs \
        npm \
        build-base \
        python3-dev \
        libffi-dev \
        openssl-dev \
        jpeg-dev \
        zlib-dev \
        freetype-dev \
        lcms2-dev \
        openjpeg-dev \
        tiff-dev \
        tk-dev \
        tcl-dev \
        harfbuzz-dev \
        fribidi-dev \
        libimagequant-dev \
        libxcb-dev \
        libpng-dev \
        sqlite \
        sqlite-dev \
    && pip3 install --no-cache-dir --upgrade pip uv

# Set working directory
WORKDIR /app

# Copy requirements and install Python packages
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# Copy application files
COPY open_notebook/ /app/open_notebook/
COPY api/ /app/api/
COPY pages/ /app/pages/
COPY migrations/ /app/migrations/
COPY commands/ /app/commands/
COPY prompts/ /app/prompts/
COPY .streamlit/ /app/.streamlit/
COPY app_home.py /app/
COPY run_api.py /app/
COPY pyproject.toml /app/
COPY supervisord.conf /app/
COPY run.sh /
COPY logo.png /app/

# Create necessary directories
RUN mkdir -p /app/data /app/logs /config/open-notebook /share/open-notebook

# Set permissions
RUN chmod a+x /run.sh

# Expose ports
EXPOSE 8501 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Labels
LABEL \
    io.hass.name="Open Notebook" \
    io.hass.description="An open source, privacy-focused alternative to Google's Notebook LM" \
    io.hass.arch="aarch64|amd64" \
    io.hass.type="addon" \
    io.hass.version="0.3.2"

# Run
CMD ["/run.sh"]
