ARG BUILD_FROM
FROM $BUILD_FROM

# Install dependencies
RUN apk add --no-cache \
    nodejs \
    npm \
    git \
    curl \
    python3 \
    make \
    g++ \
    sqlite \
    postgresql-client \
    openssl

# Install Bun
RUN curl -fsSL https://bun.sh/install | bash
ENV PATH="/root/.bun/bin:$PATH"

# Set environment with memory limits
ENV NODE_ENV=production
ENV NODE_OPTIONS="--max-old-space-size=1024"
WORKDIR /app

# Copy run script
COPY run.sh /
RUN chmod a+x /run.sh

# Expose port
EXPOSE 3000

# Run
CMD ["/run.sh"]
