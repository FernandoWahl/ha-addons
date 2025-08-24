#!/usr/bin/env python3
"""
Streamlit wrapper with proper streamlit run execution
"""

import os
import sys
import subprocess

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
    
    # Test app_home import without executing
    try:
        print("  Testing app_home availability...")
        if os.path.exists('/app/open-notebook-src/app_home.py'):
            print("  ✅ app_home.py exists")
        else:
            print("  ❌ app_home.py not found")
            return 1
    except Exception as e:
        print(f"  ❌ app_home check failed: {e}")
        return 1
    
    # Start Streamlit using proper streamlit run command
    print("🚀 Starting Streamlit with proper session context...")
    
    try:
        # Use streamlit run instead of direct import
        cmd = [
            sys.executable, '-m', 'streamlit', 'run', 'app_home.py',
            '--server.port=8502',
            '--server.address=0.0.0.0',
            '--server.headless=true',
            '--server.enableCORS=false',
            '--server.enableXsrfProtection=false',
            '--server.runOnSave=false',
            '--browser.gatherUsageStats=false'
        ]
        
        print(f"📋 Command: {' '.join(cmd)}")
        
        # Execute streamlit run
        result = subprocess.run(cmd, cwd='/app/open-notebook-src')
        return result.returncode
        
    except Exception as e:
        print(f"❌ Error starting Streamlit: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
