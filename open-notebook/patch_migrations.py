#!/usr/bin/env python3
"""
Simple patch to disable SurrealDB migrations via environment variables
"""

import os

def create_mock_surrealdb():
    """Create a mock SurrealDB module to prevent import errors"""
    mock_dir = "/app/mock_modules"
    os.makedirs(mock_dir, exist_ok=True)
    
    # Add to Python path
    import sys
    if mock_dir not in sys.path:
        sys.path.insert(0, mock_dir)
    
    # Create mock surrealdb package
    surrealdb_dir = os.path.join(mock_dir, "surrealdb")
    os.makedirs(surrealdb_dir, exist_ok=True)
    
    # Create __init__.py
    with open(os.path.join(surrealdb_dir, "__init__.py"), "w") as f:
        f.write('''"""Mock SurrealDB module for compatibility"""
class Surreal:
    def __init__(self):
        pass
    
    async def connect(self, *args, **kwargs):
        print("🚫 SurrealDB disabled - using PostgreSQL")
        raise Exception("SurrealDB disabled")
    
    async def signin(self, *args, **kwargs):
        print("🚫 SurrealDB disabled - using PostgreSQL")
        raise Exception("SurrealDB disabled")
    
    async def use(self, *args, **kwargs):
        print("🚫 SurrealDB disabled - using PostgreSQL")
        raise Exception("SurrealDB disabled")

# Make it available
surreal = Surreal()
''')
    
    # Create connections submodule
    connections_dir = os.path.join(surrealdb_dir, "connections")
    os.makedirs(connections_dir, exist_ok=True)
    
    with open(os.path.join(connections_dir, "__init__.py"), "w") as f:
        f.write("")
    
    with open(os.path.join(connections_dir, "async_ws.py"), "w") as f:
        f.write('''"""Mock async WebSocket connection"""
class AsyncWebSocketConnection:
    async def connect(self):
        raise Exception("SurrealDB disabled")
    
    async def signin(self, *args, **kwargs):
        raise Exception("SurrealDB disabled")
''')
    
    print("✅ Created mock SurrealDB module")
    return True

def set_environment_overrides():
    """Set environment variables to disable SurrealDB functionality"""
    overrides = {
        'SKIP_SURREALDB_MIGRATION': 'true',
        'USE_POSTGRESQL': 'true', 
        'DISABLE_SURREALDB': 'true',
        'SURREALDB_URL': 'disabled',
        'FORCE_POSTGRESQL': 'true'
    }
    
    for key, value in overrides.items():
        os.environ[key] = value
        print(f"✅ Set {key}={value}")
    
    return True

if __name__ == "__main__":
    print("🔧 Setting up PostgreSQL compatibility...")
    
    success1 = create_mock_surrealdb()
    success2 = set_environment_overrides()
    
    if success1 and success2:
        print("✅ PostgreSQL compatibility setup completed")
    else:
        print("⚠️ Some setup failed, but continuing...")
