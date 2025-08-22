#!/bin/bash

# ==============================================================================
# Home Assistant Add-on: SurrealDB
# SurrealDB database service for Open Notebook and other applications
# ==============================================================================

echo "=========================================="
echo "🗄️ Starting SurrealDB v1.2.1"
echo "⏰ $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================="

# Debug system and binary
echo "🔍 System Debug Information:"
echo "  Architecture: $(uname -m)"
echo "  Kernel: $(uname -r)"
echo "  OS: $(cat /etc/os-release | grep PRETTY_NAME | cut -d'"' -f2)"

echo "🔍 SurrealDB Binary Debug:"
echo "  Binary exists: $(ls -la /usr/local/bin/surreal 2>/dev/null || echo 'NOT FOUND')"
echo "  Binary format: $(file /usr/local/bin/surreal 2>/dev/null || echo 'FILE COMMAND FAILED')"
echo "  Binary size: $(stat -c%s /usr/local/bin/surreal 2>/dev/null || echo 'STAT FAILED') bytes"

# Try to identify the issue
echo "🔍 Dependency Analysis:"
if command -v ldd >/dev/null 2>&1; then
    echo "  ldd output:"
    ldd /usr/local/bin/surreal 2>&1 | head -10 || echo "  ldd failed"
else
    echo "  ldd not available"
fi

# Test execution with detailed error capture
echo "🔍 Execution Test:"
if /usr/local/bin/surreal version 2>&1; then
    echo "  ✅ SurrealDB execution successful"
else
    EXIT_CODE=$?
    echo "  ❌ SurrealDB execution failed with exit code: $EXIT_CODE"
    echo "  Trying alternative execution methods..."
    
    # Try with explicit interpreter
    if /lib/ld-musl-aarch64.so.1 /usr/local/bin/surreal version 2>&1; then
        echo "  ✅ Execution with musl loader successful"
        SURREAL_BINARY="/lib/ld-musl-aarch64.so.1 /usr/local/bin/surreal"
    else
        echo "  ❌ All execution methods failed"
        echo "  This binary may be incompatible with this Alpine Linux version"
        echo "  Attempting to continue anyway..."
        SURREAL_BINARY="/usr/local/bin/surreal"
    fi
fi

# Function to read Home Assistant configuration
read_config() {
    local key="$1"
    local default="$2"
    local value=""
    
    # Try bashio first
    if command -v bashio >/dev/null 2>&1; then
        value=$(bashio::config "$key" "$default" 2>/dev/null)
        if [[ -n "$value" && "$value" != "$default" ]]; then
            echo "$value"
            return
        fi
    fi
    
    # Fallback: try to read from options.json
    if [ -f "/data/options.json" ]; then
        value=$(python3 -c "
import json, sys
try:
    with open('/data/options.json') as f:
        data = json.load(f)
    result = data.get('$key', '$default')
    if result and result != '$default':
        print(result)
    else:
        print('$default')
except Exception as e:
    print('$default')
" 2>/dev/null)
        
        if [[ -n "$value" ]]; then
            echo "$value"
            return
        fi
    fi
    
    # Final fallback
    echo "$default"
}

# Read configuration
echo "⚙️ Reading SurrealDB configuration..."

USERNAME=$(read_config 'username' 'root')
PASSWORD=$(read_config 'password' 'root')
DATABASE=$(read_config 'database' 'open_notebook')
BIND_ADDRESS=$(read_config 'bind_address' '0.0.0.0:8000')
LOG_LEVEL=$(read_config 'log_level' 'info')
AUTH_ENABLED=$(read_config 'auth_enabled' 'true')
STORAGE_TYPE=$(read_config 'storage_type' 'memory')
DATA_PATH=$(read_config 'data_path' '/data/surrealdb')

echo "✅ Configuration loaded"

# Create data directory if using file storage
if [[ "$STORAGE_TYPE" == "file" ]]; then
    echo "📁 Creating data directory: $DATA_PATH"
    mkdir -p "$DATA_PATH"
    chmod 755 "$DATA_PATH"
fi

# Build SurrealDB command
SURREAL_CMD="${SURREAL_BINARY:-/usr/local/bin/surreal} start"

# Add bind address
SURREAL_CMD="$SURREAL_CMD --bind $BIND_ADDRESS"

# Add logging
SURREAL_CMD="$SURREAL_CMD --log $LOG_LEVEL"

# Add authentication if enabled
if [[ "$AUTH_ENABLED" == "true" ]]; then
    SURREAL_CMD="$SURREAL_CMD --user $USERNAME --pass $PASSWORD"
fi

# Add storage
case "$STORAGE_TYPE" in
    "memory")
        SURREAL_CMD="$SURREAL_CMD memory"
        echo "💾 Using in-memory storage"
        ;;
    "file")
        SURREAL_CMD="$SURREAL_CMD file://$DATA_PATH"
        echo "💾 Using file storage: $DATA_PATH"
        ;;
    "tikv")
        SURREAL_CMD="$SURREAL_CMD tikv://127.0.0.1:2379"
        echo "💾 Using TiKV storage"
        ;;
    *)
        SURREAL_CMD="$SURREAL_CMD memory"
        echo "💾 Unknown storage type, defaulting to memory"
        ;;
esac

# Show configuration summary
echo "📊 SurrealDB Configuration:"
echo "  🌐 Bind Address: $BIND_ADDRESS"
echo "  👤 Username: $USERNAME"
echo "  🔐 Password: [HIDDEN]"
echo "  🗄️ Database: $DATABASE"
echo "  📝 Log Level: $LOG_LEVEL"
echo "  🔒 Auth Enabled: $AUTH_ENABLED"
echo "  💾 Storage: $STORAGE_TYPE"
if [[ "$STORAGE_TYPE" == "file" ]]; then
    echo "  📁 Data Path: $DATA_PATH"
fi

echo "=========================================="
echo "🚀 Starting SurrealDB..."
echo "🌐 WebSocket: ws://[HOST]:8000/rpc"
echo "🌐 HTTP API: http://[HOST]:8000"
echo "📊 Health: http://[HOST]:8000/health"
echo "=========================================="

# Start SurrealDB
echo "🗄️ Executing: $SURREAL_CMD"
exec $SURREAL_CMD
