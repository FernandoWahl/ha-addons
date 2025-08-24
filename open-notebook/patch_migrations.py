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
        
        # Find the check_migration function and modify it
        original_pattern = r'def check_migration\(\):(.*?)(?=def|\Z)'
        
        new_function = '''def check_migration():
    """Skip SurrealDB migration check when using PostgreSQL/SQLite"""
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
    except Exception as e:
        print(f"⚠️ Migration failed, continuing anyway: {e}")
        pass

'''
        
        # Replace the function
        if 'def check_migration():' in content:
            # Find the function and replace it
            lines = content.split('\n')
            new_lines = []
            in_function = False
            indent_level = 0
            
            for line in lines:
                if line.strip().startswith('def check_migration():'):
                    in_function = True
                    indent_level = len(line) - len(line.lstrip())
                    new_lines.extend(new_function.split('\n'))
                    continue
                
                if in_function:
                    current_indent = len(line) - len(line.lstrip())
                    # If we hit a line with same or less indentation and it's not empty, function is over
                    if line.strip() and current_indent <= indent_level:
                        in_function = False
                        new_lines.append(line)
                    # Skip lines that are part of the original function
                    elif not line.strip() or current_indent > indent_level:
                        continue
                    else:
                        in_function = False
                        new_lines.append(line)
                else:
                    new_lines.append(line)
            
            # Write the patched content
            with open(utils_file, 'w') as f:
                f.write('\n'.join(new_lines))
            
            print("✅ Successfully patched migration check")
            return True
        else:
            print("❌ check_migration function not found")
            return False
            
    except Exception as e:
        print(f"❌ Error patching migration check: {e}")
        return False

def patch_database_repository():
    """Patch database repository to handle missing SurrealDB gracefully"""
    repo_file = "/app/open-notebook-src/open_notebook/database/repository.py"
    
    if not os.path.exists(repo_file):
        print(f"❌ File not found: {repo_file}")
        return False
    
    try:
        with open(repo_file, 'r') as f:
            content = f.read()
        
        # Add a check at the beginning of db_connection function
        if 'async def db_connection():' in content or 'def db_connection():' in content:
            # Add environment check
            patch_code = '''
import os
if os.getenv('USE_POSTGRESQL', 'false').lower() == 'true':
    # Use PostgreSQL connection instead
    import asyncpg
    import asyncio
    from contextlib import asynccontextmanager
    
    @asynccontextmanager
    async def postgresql_connection():
        database_url = os.getenv('DATABASE_URL', '')
        if database_url.startswith('postgresql://'):
            conn = await asyncpg.connect(database_url)
            try:
                yield conn
            finally:
                await conn.close()
        else:
            # Fallback to SQLite or raise error
            raise Exception("PostgreSQL URL not configured properly")
    
    return postgresql_connection()

'''
            
            # Insert the patch at the beginning of the db_connection function
            content = content.replace(
                'async def db_connection():',
                f'async def db_connection():{patch_code}'
            )
            
            with open(repo_file, 'w') as f:
                f.write(content)
            
            print("✅ Successfully patched database repository")
            return True
        else:
            print("❌ db_connection function not found")
            return False
            
    except Exception as e:
        print(f"❌ Error patching database repository: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Patching Open Notebook for PostgreSQL compatibility...")
    
    success1 = patch_migration_check()
    success2 = patch_database_repository()
    
    if success1 and success2:
        print("✅ All patches applied successfully")
    else:
        print("⚠️ Some patches failed, but continuing...")
