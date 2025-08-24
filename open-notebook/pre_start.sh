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
echo "🐍 Environment configured for PostgreSQL"
echo "🗄️ Database mode: PostgreSQL"
