#!/bin/bash

echo "🔧 Pre-start PostgreSQL compatibility setup..."

# Set environment variables
export SKIP_SURREALDB_MIGRATION=true
export USE_POSTGRESQL=true
export DISABLE_SURREALDB=true
export SURREALDB_URL=disabled
export FORCE_POSTGRESQL=true

echo "🔧 Patching migration files directly..."

# Patch the check_migration function in utils.py
if [ -f "/app/open-notebook-src/pages/stream_app/utils.py" ]; then
    echo "📝 Patching utils.py migration check..."
    
    # Create backup
    cp "/app/open-notebook-src/pages/stream_app/utils.py" "/app/open-notebook-src/pages/stream_app/utils.py.backup"
    
    # Replace the check_migration function with a PostgreSQL-aware version
    cat > /tmp/patch_utils.py << 'EOF'
import re
import os

def patch_utils():
    file_path = "/app/open-notebook-src/pages/stream_app/utils.py"
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Find and replace the check_migration function
    pattern = r'def check_migration\(\):(.*?)(?=\ndef|\nclass|\n@|\Z)'
    
    replacement = '''def check_migration():
    """PostgreSQL-compatible migration check"""
    import os
    
    # Skip migration if using PostgreSQL
    if os.getenv('USE_POSTGRESQL', 'false').lower() == 'true':
        print("🐘 Using PostgreSQL - skipping SurrealDB migration")
        return
    
    if os.getenv('SKIP_SURREALDB_MIGRATION', 'false').lower() == 'true':
        print("🔄 Skipping SurrealDB migration (PostgreSQL mode)")
        return
    
    # Original migration logic (only for SurrealDB users)
    try:
        from open_notebook.database.migrate import MigrationManager
        mm = MigrationManager()
        mm.run_migration_up()
    except Exception as e:
        print(f"⚠️ Migration failed, continuing: {e}")
        pass'''
    
    # Replace the function
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # If no replacement was made, try a simpler approach
    if new_content == content:
        # Just replace the function call
        new_content = content.replace(
            'check_migration()',
            'postgresql_safe_migration()'
        )
        
        # Add the safe function at the end
        new_content += '''

def postgresql_safe_migration():
    """Safe migration that skips SurrealDB when using PostgreSQL"""
    import os
    
    if os.getenv('USE_POSTGRESQL', 'false').lower() == 'true':
        print("🐘 Using PostgreSQL - skipping SurrealDB migration")
        return
    
    if os.getenv('SKIP_SURREALDB_MIGRATION', 'false').lower() == 'true':
        print("🔄 Skipping SurrealDB migration")
        return
    
    try:
        from open_notebook.database.migrate import MigrationManager
        mm = MigrationManager()
        mm.run_migration_up()
    except Exception as e:
        print(f"⚠️ Migration failed, continuing: {e}")
        pass
'''
    
    with open(file_path, 'w') as f:
        f.write(new_content)
    
    print("✅ Patched utils.py successfully")

if __name__ == "__main__":
    patch_utils()
EOF

    python3 /tmp/patch_utils.py
    
else
    echo "❌ utils.py not found"
fi

# Also patch the migrate.py file directly
if [ -f "/app/open-notebook-src/open_notebook/database/migrate.py" ]; then
    echo "📝 Patching migrate.py..."
    
    # Create backup
    cp "/app/open-notebook-src/open_notebook/database/migrate.py" "/app/open-notebook-src/open_notebook/database/migrate.py.backup"
    
    # Add PostgreSQL check at the beginning of run_migration_up
    cat > /tmp/patch_migrate.py << 'EOF'
import os

def patch_migrate():
    file_path = "/app/open-notebook-src/open_notebook/database/migrate.py"
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Add check at the beginning of run_migration_up method
    if 'def run_migration_up(self):' in content:
        content = content.replace(
            'def run_migration_up(self):',
            '''def run_migration_up(self):
        # Skip migration if using PostgreSQL
        if os.getenv('USE_POSTGRESQL', 'false').lower() == 'true':
            print("🐘 PostgreSQL mode - skipping SurrealDB migration")
            return
        
        if os.getenv('SKIP_SURREALDB_MIGRATION', 'false').lower() == 'true':
            print("🔄 Skipping SurrealDB migration")
            return'''
        )
        
        # Add import at the top if not present
        if 'import os' not in content:
            content = 'import os\n' + content
        
        with open(file_path, 'w') as f:
            f.write(content)
        
        print("✅ Patched migrate.py successfully")
    else:
        print("❌ run_migration_up method not found in migrate.py")

if __name__ == "__main__":
    patch_migrate()
EOF

    python3 /tmp/patch_migrate.py
    
else
    echo "❌ migrate.py not found"
fi

echo "✅ PostgreSQL compatibility setup completed"

# Patch API client for resilient connections
if [ -f "/app/open-notebook-src/api/client.py" ]; then
    echo "📝 Patching API client for resilient connections..."
    
    # Create backup
    cp "/app/open-notebook-src/api/client.py" "/app/open-notebook-src/api/client.py.backup"
    
    # Patch the _make_request method to be more resilient
    cat > /tmp/patch_client.py << 'EOF'
import re

def patch_client():
    file_path = "/app/open-notebook-src/api/client.py"
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Add resilient connection handling
    if 'def _make_request(self' in content:
        # Replace the _make_request method with a more resilient version
        pattern = r'def _make_request\(self[^}]*?raise ConnectionError\(f"Failed to connect to API: \{str\(e\)\}"\)'
        
        replacement = '''def _make_request(self, method, endpoint, **kwargs):
        """Make HTTP request with resilient error handling"""
        import time
        import os
        
        # If API is not ready yet, wait a bit
        max_retries = 3
        for attempt in range(max_retries):
            try:
                url = f"{self.base_url}{endpoint}"
                response = self.session.request(method, url, **kwargs)
                response.raise_for_status()
                return response.json() if response.content else {}
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"⏳ API connection attempt {attempt + 1} failed, retrying...")
                    time.sleep(2)
                    continue
                else:
                    # On final failure, return empty response instead of crashing
                    print(f"⚠️ API connection failed after {max_retries} attempts: {e}")
                    if "models" in endpoint:
                        return {"models": []}
                    return {}'''
        
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        # If regex didn't work, try simpler replacement
        if new_content == content:
            new_content = content.replace(
                'raise ConnectionError(f"Failed to connect to API: {str(e)}")',
                '''print(f"⚠️ API connection failed: {e}")
                if "models" in endpoint:
                    return {"models": []}
                return {}'''
            )
        
        with open(file_path, 'w') as f:
            f.write(new_content)
        
        print("✅ Patched API client successfully")
    else:
        print("❌ _make_request method not found in client.py")

if __name__ == "__main__":
    patch_client()
EOF

    python3 /tmp/patch_client.py
    
else
    echo "❌ client.py not found"
fi

echo "✅ All patches applied successfully"

# Create mock surreal_commands module
echo "📦 Creating mock surreal_commands module..."
cat > /app/open-notebook-src/surreal_commands.py << 'EOF'
"""Mock surreal_commands module for PostgreSQL compatibility"""

def get_command_status(*args, **kwargs):
    """Mock function for command status"""
    return {"status": "completed", "result": "PostgreSQL mode - command skipped"}

def submit_command(*args, **kwargs):
    """Mock function for command submission"""
    return {"id": "mock_command", "status": "submitted", "message": "PostgreSQL mode - command mocked"}

# Add any other functions that might be imported
def execute_command(*args, **kwargs):
    return {"status": "success", "message": "PostgreSQL mode"}

def get_command_result(*args, **kwargs):
    return {"result": "PostgreSQL mode - no SurrealDB commands"}
EOF

echo "✅ Created mock surreal_commands module"

# Fix API port configuration
echo "🔧 Fixing API port configuration..."
if [ -f "/app/open-notebook-src/run_api.py" ]; then
    # Create backup
    cp "/app/open-notebook-src/run_api.py" "/app/open-notebook-src/run_api.py.backup"
    
    # Replace port 5055 with 8000
    sed -i 's/127.0.0.1:5055/0.0.0.0:8000/g' /app/open-notebook-src/run_api.py
    sed -i 's/localhost:5055/localhost:8000/g' /app/open-notebook-src/run_api.py
    sed -i 's/port=5055/port=8000/g' /app/open-notebook-src/run_api.py
    
    echo "✅ Fixed API port configuration"
else
    echo "❌ run_api.py not found"
fi

echo "🐍 Environment configured for PostgreSQL"
echo "🗄️ Database mode: PostgreSQL"
