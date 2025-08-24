#!/bin/bash

echo "🔧 Pre-start PostgreSQL compatibility setup..."

# Set environment variables
export SKIP_SURREALDB_MIGRATION=true
export USE_POSTGRESQL=true
export DISABLE_SURREALDB=true
export SURREALDB_URL=disabled
export FORCE_POSTGRESQL=true

# Create mock modules directory
mkdir -p /app/mock_modules/surrealdb/connections

# Create mock SurrealDB __init__.py
cat > /app/mock_modules/surrealdb/__init__.py << 'EOF'
"""Mock SurrealDB module for compatibility"""
import os

class MockSurreal:
    def __init__(self):
        pass
    
    async def connect(self, *args, **kwargs):
        if os.getenv('USE_POSTGRESQL', 'false').lower() == 'true':
            print("🚫 SurrealDB disabled - using PostgreSQL")
            raise Exception("SurrealDB disabled - using PostgreSQL")
        return self
    
    async def signin(self, *args, **kwargs):
        if os.getenv('USE_POSTGRESQL', 'false').lower() == 'true':
            print("🚫 SurrealDB disabled - using PostgreSQL")
            raise Exception("SurrealDB disabled - using PostgreSQL")
        return True
    
    async def use(self, *args, **kwargs):
        if os.getenv('USE_POSTGRESQL', 'false').lower() == 'true':
            print("🚫 SurrealDB disabled - using PostgreSQL")
            raise Exception("SurrealDB disabled - using PostgreSQL")
        return True

# Create instance
Surreal = MockSurreal
EOF

# Create mock connections module
cat > /app/mock_modules/surrealdb/connections/__init__.py << 'EOF'
"""Mock connections module"""
EOF

cat > /app/mock_modules/surrealdb/connections/async_ws.py << 'EOF'
"""Mock async WebSocket connection"""
import os

class AsyncWebSocketConnection:
    async def connect(self):
        if os.getenv('USE_POSTGRESQL', 'false').lower() == 'true':
            raise Exception("SurrealDB disabled - using PostgreSQL")
        return self
    
    async def signin(self, *args, **kwargs):
        if os.getenv('USE_POSTGRESQL', 'false').lower() == 'true':
            raise Exception("SurrealDB disabled - using PostgreSQL")
        return True
EOF

# Add mock modules to Python path
export PYTHONPATH="/app/mock_modules:$PYTHONPATH"

echo "✅ PostgreSQL compatibility setup completed"
echo "🐍 PYTHONPATH: $PYTHONPATH"
echo "🗄️ Database mode: PostgreSQL"
