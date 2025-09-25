ARG BUILD_FROM
FROM $BUILD_FROM

# Install dependencies
RUN apk add --no-cache \
    nodejs \
    npm \
    git \
    curl \
    postgresql-client \
    python3 \
    make \
    g++ \
    && curl -fsSL https://bun.sh/install | bash

# Set environment variables
ENV PATH="/root/.bun/bin:$PATH"
ENV NODE_ENV=production

# Create app directory
WORKDIR /app

# Clone Blinko as submodule (will be handled by run script)
COPY run.sh /
RUN chmod a+x /run.sh

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:3000/api/health || exit 1

# Run
CMD ["/run.sh"]
