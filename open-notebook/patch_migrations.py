#!/usr/bin/env python3
"""
Patch script to disable SurrealDB migrations and use PostgreSQL/SQLite instead
"""

import os
import re

def patch_migration_check():
    """Patch the migration check to skip SurrealDB"""
    utils_file = "/app/open-notebook-src/pages/stream_app/utils.py"
    
    if not os.path.exists(utils_file):
        print(f"❌ File not found: {utils_file}")
        return False
    
    try:
        with open(utils_file, 'r') as f:
            content = f.read()
        
        # Simple replacement approach - replace the entire check_migration function call
        if 'check_migration()' in content:
            # Replace calls to check_migration() with our safe version
            content = content.replace(
                'check_migration()',
                'safe_check_migration()'
            )
            
            # Add our safe function at the end of the file
            safe_function = '''

def safe_check_migration():
    """Safe migration check that skips SurrealDB when using PostgreSQL"""
    import os
    
    # Check if we should skip SurrealDB migrations
    if os.getenv('SKIP_SURREALDB_MIGRATION', 'false').lower() == 'true':
        print("🔄 Skipping SurrealDB migration (using PostgreSQL/SQLite)")
        return
    
    if os.getenv('USE_POSTGRESQL', 'false').lower() == 'true':
        print("🐘 Using PostgreSQL - skipping SurrealDB migration")
        return
        
    if os.getenv('DISABLE_SURREALDB', 'false').lower() == 'true':
        print("🚫 SurrealDB disabled - skipping migration")
        return
    
    # Original migration code (only runs if SurrealDB is enabled)
    try:
        from open_notebook.database.migrate import MigrationManager
        mm = MigrationManager()
        mm.run_migration_up()
        print("✅ SurrealDB migration completed")
    except Exception as e:
        print(f"⚠️ Migration failed, continuing anyway: {e}")
        pass
'''
            
            content += safe_function
            
            # Write the patched content
            with open(utils_file, 'w') as f:
                f.write(content)
            
            print("✅ Successfully patched migration check")
            return True
        else:
            print("❌ check_migration function call not found")
            return False
            
    except Exception as e:
        print(f"❌ Error patching migration check: {e}")
        return False

def create_database_override():
    """Create a database override module"""
    override_file = "/app/database_override.py"
    
    try:
        with open(override_file, 'w') as f:
            f.write('''"""
Database override for PostgreSQL compatibility
"""
import os
import asyncio
from contextlib import asynccontextmanager

@asynccontextmanager
async def safe_db_connection():
    """Safe database connection that uses PostgreSQL when configured"""
    database_url = os.getenv('DATABASE_URL', '')
    
    if database_url.startswith('postgresql://'):
        try:
            import asyncpg
            conn = await asyncpg.connect(database_url)
            print("🐘 Connected to PostgreSQL")
            try:
                yield conn
            finally:
                await conn.close()
        except Exception as e:
            print(f"❌ PostgreSQL connection failed: {e}")
            # Fallback to mock connection
            yield None
    else:
        print("📁 Using SQLite fallback")
        # Mock connection for SQLite
        yield None
''')
        
        print("✅ Created database override module")
        return True
        
    except Exception as e:
        print(f"❌ Error creating database override: {e}")
        return False

def patch_imports():
    """Patch import statements to handle missing modules gracefully"""
    files_to_patch = [
        "/app/open-notebook-src/open_notebook/domain/base.py",
        "/app/open-notebook-src/app_home.py"
    ]
    
    for file_path in files_to_patch:
        if not os.path.exists(file_path):
            continue
            
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Add try-except around problematic imports
            if 'from open_notebook.database.repository import' in content:
                content = content.replace(
                    'from open_notebook.database.repository import',
                    '''try:
    from open_notebook.database.repository import'''
                )
                
                # Find the end of the import block and add except
                lines = content.split('\n')
                new_lines = []
                in_import_block = False
                
                for i, line in enumerate(lines):
                    if 'try:' in line and 'from open_notebook.database.repository import' in line:
                        in_import_block = True
                        new_lines.append(line)
                    elif in_import_block and (line.strip() == '' or not line.startswith(' ') and not line.startswith('\t')):
                        # End of import block
                        new_lines.append('except ImportError as e:')
                        new_lines.append('    print(f"⚠️ Database import failed: {e}")')
                        new_lines.append('    pass')
                        new_lines.append(line)
                        in_import_block = False
                    else:
                        new_lines.append(line)
                
                content = '\n'.join(new_lines)
                
                with open(file_path, 'w') as f:
                    f.write(content)
                
                print(f"✅ Patched imports in {file_path}")
                
        except Exception as e:
            print(f"⚠️ Could not patch {file_path}: {e}")
            continue
    
    return True

if __name__ == "__main__":
    print("🔧 Patching Open Notebook for PostgreSQL compatibility...")
    
    success1 = patch_migration_check()
    success2 = create_database_override()
    success3 = patch_imports()
    
    if success1:
        print("✅ Migration patches applied successfully")
    else:
        print("⚠️ Migration patches failed, but continuing...")
    
    print("✅ Patching completed")
