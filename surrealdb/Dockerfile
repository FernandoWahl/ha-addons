ARG BUILD_FROM
FROM $BUILD_FROM

# Install curl and debugging tools
RUN apk add --no-cache curl file ldd

# Install SurrealDB and find where it was installed
RUN curl -sSf https://install.surrealdb.com | sh && \
    find / -name "surreal" -type f 2>/dev/null | head -5 && \
    ls -la /usr/local/bin/ && \
    ls -la /root/.surrealdb/ 2>/dev/null || echo "No .surrealdb directory"

# Try to find and move SurrealDB to the correct location
RUN if [ -f /root/.surrealdb/surreal ]; then \
        cp /root/.surrealdb/surreal /usr/local/bin/surreal && \
        chmod +x /usr/local/bin/surreal; \
    elif [ -f /usr/local/bin/surreal ]; then \
        chmod +x /usr/local/bin/surreal; \
    else \
        echo "SurrealDB binary not found in expected locations"; \
        exit 1; \
    fi

# Debug the binary
RUN echo "=== DEBUGGING SURREAL BINARY ===" && \
    ls -la /usr/local/bin/surreal && \
    file /usr/local/bin/surreal && \
    ldd /usr/local/bin/surreal || echo "ldd failed - static binary or missing libs" && \
    echo "=== TRYING TO EXECUTE ===" && \
    /usr/local/bin/surreal version || echo "Execution failed"

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
