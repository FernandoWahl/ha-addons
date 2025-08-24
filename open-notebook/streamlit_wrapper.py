#!/usr/bin/env python3
"""
Streamlit wrapper with error handling and debugging
"""

import os
import sys
import traceback
import subprocess

def main():
    print("🌐 Streamlit Wrapper Starting...")
    print(f"🐍 Python version: {sys.version}")
    print(f"📁 Working directory: {os.getcwd()}")
    print(f"🔧 PYTHONPATH: {os.getenv('PYTHONPATH', 'Not set')}")
    
    # Check environment
    print("🌍 Environment check:")
    for key in ['USE_POSTGRESQL', 'DATABASE_URL', 'SKIP_SURREALDB_MIGRATION']:
        value = os.getenv(key, 'Not set')
        print(f"  {key}: {value}")
    
    # Check if files exist
    print("📁 File check:")
    files_to_check = [
        '/app/open-notebook-src/app_home.py',
        '/app/open-notebook-src/pages/stream_app/utils.py',
        '/app/open-notebook-src/open_notebook/database/migrate.py'
    ]
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path}")
    
    # Check if patches were applied
    print("🔧 Patch verification:")
    try:
        with open('/app/open-notebook-src/pages/stream_app/utils.py', 'r') as f:
            content = f.read()
            if 'USE_POSTGRESQL' in content:
                print("  ✅ utils.py patched")
            else:
                print("  ❌ utils.py not patched")
    except Exception as e:
        print(f"  ❌ Error checking utils.py: {e}")
    
    try:
        with open('/app/open-notebook-src/open_notebook/database/migrate.py', 'r') as f:
            content = f.read()
            if 'USE_POSTGRESQL' in content:
                print("  ✅ migrate.py patched")
            else:
                print("  ❌ migrate.py not patched")
    except Exception as e:
        print(f"  ❌ Error checking migrate.py: {e}")
    
    # Try to import modules
    print("📦 Module import test:")
    try:
        import streamlit
        print(f"  ✅ streamlit: {streamlit.__version__}")
    except Exception as e:
        print(f"  ❌ streamlit import failed: {e}")
        return 1
    
    try:
        sys.path.insert(0, '/app/open-notebook-src')
        from open_notebook.domain.base import ObjectModel
        print("  ✅ open_notebook.domain.base imported")
    except Exception as e:
        print(f"  ❌ open_notebook.domain.base import failed: {e}")
        print(f"  📋 Traceback: {traceback.format_exc()}")
    
    # Start Streamlit
    print("🚀 Starting Streamlit...")
    try:
        cmd = [
            sys.executable, '-m', 'streamlit', 'run', 'app_home.py',
            '--server.port=8501',
            '--server.address=0.0.0.0',
            '--server.headless=true',
            '--server.enableCORS=false',
            '--server.enableXsrfProtection=false'
        ]
        
        print(f"📋 Command: {' '.join(cmd)}")
        
        # Change to the correct directory
        os.chdir('/app/open-notebook-src')
        
        # Run Streamlit
        result = subprocess.run(cmd, capture_output=False)
        return result.returncode
        
    except Exception as e:
        print(f"❌ Error starting Streamlit: {e}")
        print(f"📋 Traceback: {traceback.format_exc()}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
