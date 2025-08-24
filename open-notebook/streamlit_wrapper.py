#!/usr/bin/env python3
"""
Streamlit wrapper with focused error detection
"""

import os
import sys
import traceback

def main():
    print("🌐 STREAMLIT WRAPPER: Starting debug...")
    
    # Set working directory
    os.chdir('/app/open-notebook-src')
    print(f"📁 Working directory: {os.getcwd()}")
    
    # Check critical environment variables
    print("🌍 Critical environment:")
    print(f"  USE_POSTGRESQL: {os.getenv('USE_POSTGRESQL', 'NOT SET')}")
    print(f"  SKIP_SURREALDB_MIGRATION: {os.getenv('SKIP_SURREALDB_MIGRATION', 'NOT SET')}")
    
    # Test critical imports
    print("📦 Testing critical imports...")
    
    try:
        print("  Testing streamlit import...")
        import streamlit as st
        print(f"  ✅ Streamlit {st.__version__} imported successfully")
    except Exception as e:
        print(f"  ❌ Streamlit import failed: {e}")
        return 1
    
    try:
        print("  Testing app_home import...")
        sys.path.insert(0, '/app/open-notebook-src')
        
        # Try to import the main app file
        import app_home
        print("  ✅ app_home imported successfully")
    except Exception as e:
        print(f"  ❌ app_home import failed: {e}")
        print(f"  📋 Full traceback:")
        traceback.print_exc()
        
        # Try to identify the specific issue
        if "surrealdb" in str(e).lower():
            print("  🔍 Issue appears to be SurrealDB related")
        elif "migration" in str(e).lower():
            print("  🔍 Issue appears to be migration related")
        elif "database" in str(e).lower():
            print("  🔍 Issue appears to be database related")
        
        return 1
    
    # If we get here, try to run Streamlit
    print("🚀 All imports successful - starting Streamlit...")
    
    try:
        # Use exec to replace the process
        os.execvp(sys.executable, [
            sys.executable, '-m', 'streamlit', 'run', 'app_home.py',
            '--server.port=8501',
            '--server.address=0.0.0.0',
            '--server.headless=true',
            '--server.enableCORS=false',
            '--server.enableXsrfProtection=false'
        ])
    except Exception as e:
        print(f"❌ Failed to start Streamlit: {e}")
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
