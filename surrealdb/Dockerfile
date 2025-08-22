ARG BUILD_FROM
FROM $BUILD_FROM

# Install curl and glibc compatibility for SurrealDB
RUN apk add --no-cache curl && \
    # Install glibc compatibility layer for Alpine
    wget -q -O /etc/apk/keys/sgerrand.rsa.pub https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub && \
    wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.34-r0/glibc-2.34-r0.apk && \
    wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.34-r0/glibc-bin-2.34-r0.apk && \
    apk add --no-cache --force-overwrite glibc-2.34-r0.apk glibc-bin-2.34-r0.apk && \
    rm glibc-2.34-r0.apk glibc-bin-2.34-r0.apk

# Install SurrealDB
RUN curl -sSf https://install.surrealdb.com | sh

# Verify SurrealDB installation
RUN /usr/local/bin/surreal version

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
