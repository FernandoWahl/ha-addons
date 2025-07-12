ARG BUILD_FROM
FROM $BUILD_FROM

# Set shell
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Install Python and dependencies
RUN \
    apk add --no-cache \
        python3 \
        py3-pip \
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
    && apk add --no-cache --virtual .build-deps \
        gcc \
        musl-dev \
        python3-dev \
        libffi-dev \
        openssl-dev \
        cargo \
        rust \
    && pip3 install --no-cache-dir --upgrade pip

# Copy requirements and install Python packages
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# Remove build dependencies
RUN apk del .build-deps

# Copy application files
COPY app.py /app/
COPY run.sh /
RUN chmod a+x /run.sh

# Set working directory
WORKDIR /app

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Labels
LABEL \
    io.hass.name="Image Combiner" \
    io.hass.description="API service to combine up to 4 images into a single composite image" \
    io.hass.arch="armhf|aarch64|amd64|armv7|i386" \
    io.hass.type="addon" \
    io.hass.version="1.0.0"

# Run
CMD ["/run.sh"]
