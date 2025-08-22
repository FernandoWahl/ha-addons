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
    git \
    && pip3 install --no-cache-dir --upgrade pip

# Set working directory
WORKDIR /app

# Clone the original Open Notebook repository
RUN git clone https://github.com/lfnovo/open-notebook.git open-notebook-src

# Install core dependencies first (ARM64 compatible versions)
RUN pip3 install --no-cache-dir \
    --index-url https://pypi.org/simple \
    --prefer-binary \
    "streamlit>=1.45.0" \
    "fastapi>=0.104.0" \
    "uvicorn>=0.24.0" \
    "pydantic>=2.5.0,<2.9.0" \
    "loguru>=0.7.2" \
    "python-dotenv>=1.0.1" \
    "httpx>=0.27.0" \
    "supervisor>=4.2.5" \
    "requests>=2.31.0"

# Install LangChain ecosystem with compatible versions
RUN pip3 install --no-cache-dir \
    --index-url https://pypi.org/simple \
    --prefer-binary \
    "langchain>=0.1.0,<0.3.0" \
    "langchain-core>=0.1.0,<0.3.0" \
    "langchain-community>=0.0.1,<0.3.0" \
    "langchain-openai>=0.1.0,<0.2.0" \
    "langchain-anthropic>=0.1.0,<0.2.0" \
    "langchain-groq>=0.1.0,<0.2.0" \
    "langchain-google-genai>=1.0.0,<2.1.0" \
    "langchain-ollama>=0.1.0,<0.2.0" \
    "tiktoken>=0.5.0"

# Install Streamlit components
RUN pip3 install --no-cache-dir \
    --index-url https://pypi.org/simple \
    --prefer-binary \
    "streamlit-tags>=1.2.8" \
    "streamlit-scrollable-textbox>=0.0.3" \
    "streamlit-monaco>=0.1.3"

# Install database and advanced dependencies
RUN pip3 install --no-cache-dir \
    --index-url https://pypi.org/simple \
    --prefer-binary \
    "surrealdb>=1.0.0" \
    "surreal-commands>=1.0.0" \
    "humanize>=4.11.0" \
    "tomli>=2.0.2" \
    "groq>=0.12.0" \
    "nest-asyncio>=1.6.0"

# Install additional dependencies that might be needed
RUN pip3 install --no-cache-dir \
    --index-url https://pypi.org/simple \
    --prefer-binary \
    "content-core>=1.0.0" \
    "ai-prompter>=0.3" \
    "esperanto>=2.3.0" \
    "podcast-creator>=0.2.0" || echo "Optional packages failed, continuing..."

# Try to install LangGraph (might fail on ARM64, so optional)
RUN pip3 install --no-cache-dir \
    --index-url https://pypi.org/simple \
    --prefer-binary \
    "langgraph>=0.1.0,<0.3.0" \
    "langgraph-checkpoint-sqlite>=1.0.0,<3.0.0" || echo "LangGraph failed, continuing without it..."

# Install remaining LangChain providers (optional)
RUN pip3 install --no-cache-dir \
    --index-url https://pypi.org/simple \
    --prefer-binary \
    "langchain_mistralai>=0.1.0,<0.3.0" \
    "langchain_deepseek>=0.1.0,<0.2.0" \
    "langchain-google-vertexai>=1.0.0,<3.0.0" || echo "Some LangChain providers failed, continuing..."

# Try to install the full package without dependencies (since we installed them manually)
WORKDIR /app/open-notebook-src
RUN pip3 install --no-cache-dir --no-deps -e .

# Go back to app directory
WORKDIR /app

# Copy only our interface files
COPY run.sh /
COPY supervisord_interface.conf /app/supervisord.conf

# Create directories for Home Assistant integration
RUN mkdir -p /app/logs /config/open-notebook /share/open-notebook

# Set permissions
RUN chmod +x /run.sh

# Expose ports
EXPOSE 8501 8000

# Health check
HEALTHCHECK --interval=60s --timeout=30s --start-period=300s --retries=3 \
    CMD curl -f http://localhost:8501 || exit 1

# Run our interface script
CMD ["/run.sh"]
