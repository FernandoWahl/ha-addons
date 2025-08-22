ARG BUILD_FROM
FROM $BUILD_FROM

# Install dependencies
RUN apk add --no-cache curl tar file

# Download SurrealDB static binary directly for ARM64
RUN SURREAL_VERSION="2.3.7" && \
    curl -L "https://github.com/surrealdb/surrealdb/releases/download/v${SURREAL_VERSION}/surreal-v${SURREAL_VERSION}.linux-arm64.tgz" -o surreal.tgz && \
    tar -xzf surreal.tgz && \
    mv surreal /usr/local/bin/surreal && \
    chmod +x /usr/local/bin/surreal && \
    rm surreal.tgz

# Verify binary exists and check format (but don't execute during build)
RUN echo "SurrealDB binary installed:" && \
    ls -la /usr/local/bin/surreal && \
    file /usr/local/bin/surreal && \
    echo "Binary will be tested at runtime"

# Copy run script
COPY run.sh /
RUN chmod +x /run.sh

# Create data directory
RUN mkdir -p /data/surrealdb

# Expose SurrealDB port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run SurrealDB
CMD ["/run.sh"]
