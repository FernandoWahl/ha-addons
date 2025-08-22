ARG BUILD_FROM
FROM $BUILD_FROM

# Install curl for SurrealDB installation
RUN apk add --no-cache curl

# Install SurrealDB (it installs directly to /usr/local/bin/surreal)
RUN curl -sSf https://install.surrealdb.com | sh

# Verify SurrealDB installation
RUN surreal version

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
