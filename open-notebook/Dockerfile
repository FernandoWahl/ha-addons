ARG BUILD_FROM
FROM $BUILD_FROM

# Install system dependencies
RUN apk add --no-cache \
    python3 \
    py3-pip \
    curl \
    supervisor \
    && pip3 install --no-cache-dir --upgrade pip

# Set working directory
WORKDIR /app

# Copy and install requirements
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# Copy essential application files
COPY app_home_working.py /app/app_home.py
COPY run.sh /
COPY supervisord.conf /app/

# Create a simple FastAPI app for now
RUN echo 'from fastapi import FastAPI\napp = FastAPI()\n@app.get("/")\ndef read_root():\n    return {"message": "Open Notebook API"}' > /app/run_api.py

# Create directories
RUN mkdir -p /app/logs /config/open-notebook /share/open-notebook

# Set permissions
RUN chmod +x /run.sh

# Expose ports
EXPOSE 8501 8000

# Health check
HEALTHCHECK --interval=60s --timeout=30s --start-period=120s --retries=2 \
    CMD curl -f http://localhost:8501 || exit 1

# Run
CMD ["/run.sh"]
