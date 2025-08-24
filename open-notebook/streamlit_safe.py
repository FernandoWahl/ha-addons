#!/usr/bin/env python3
"""
Safe Streamlit execution wrapper to avoid SIGILL issues.
This version uses alternative execution methods to prevent illegal instruction errors.
"""

import os
import sys
import subprocess
import signal
import time
from pathlib import Path

def setup_environment():
    """Setup environment for safe Streamlit execution."""
    print("🔧 Setting up safe Streamlit environment...")
    
    # Set environment variables for safer execution
    os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
    os.environ['STREAMLIT_SERVER_ENABLE_CORS'] = 'false'
    os.environ['STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION'] = 'false'
    os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
    os.environ['STREAMLIT_SERVER_RUN_ON_SAVE'] = 'false'
    
    # Disable problematic features that might cause SIGILL
    os.environ['STREAMLIT_SERVER_ENABLE_WEBSOCKET_COMPRESSION'] = 'false'
    os.environ['STREAMLIT_SERVER_MAX_UPLOAD_SIZE'] = '1'
    os.environ['STREAMLIT_GLOBAL_DEVELOPMENT_MODE'] = 'false'
    
    # Set Python optimization flags
    os.environ['PYTHONOPTIMIZE'] = '1'
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
    
    print("✅ Environment configured for safe execution")

def run_streamlit_subprocess():
    """Run Streamlit using subprocess with safe parameters."""
    print("🚀 Starting Streamlit via subprocess...")
    
    cmd = [
        sys.executable, '-m', 'streamlit', 'run', 'app_home.py',
        '--server.port=8502',
        '--server.address=0.0.0.0',
        '--server.headless=true',
        '--server.enableCORS=false',
        '--server.enableXsrfProtection=false',
        '--server.runOnSave=false',
        '--browser.gatherUsageStats=false',
        '--server.enableWebsocketCompression=false',
        '--global.developmentMode=false'
    ]
    
    try:
        # Use exec to replace the current process
        os.execvp(sys.executable, cmd)
    except Exception as e:
        print(f"❌ Subprocess execution failed: {e}")
        return False

def run_streamlit_direct():
    """Run Streamlit by directly importing and calling main."""
    print("🚀 Starting Streamlit via direct import...")
    
    try:
        # Import streamlit and run directly
        import streamlit.web.cli as stcli
        
        # Set sys.argv for streamlit
        sys.argv = [
            'streamlit', 'run', 'app_home.py',
            '--server.port=8502',
            '--server.address=0.0.0.0',
            '--server.headless=true',
            '--server.enableCORS=false',
            '--server.enableXsrfProtection=false',
            '--server.runOnSave=false',
            '--browser.gatherUsageStats=false',
            '--server.enableWebsocketCompression=false',
            '--global.developmentMode=false'
        ]
        
        # Call streamlit main
        stcli.main()
        
    except Exception as e:
        print(f"❌ Direct import execution failed: {e}")
        return False

def run_streamlit_minimal():
    """Run a minimal Streamlit server to avoid SIGILL issues."""
    print("🚀 Starting minimal Streamlit server...")
    
    try:
        import streamlit as st
        from streamlit.web import bootstrap
        
        # Minimal bootstrap
        bootstrap.run(
            'app_home.py',
            command_line='',
            args=[],
            flag_options={}
        )
        
    except Exception as e:
        print(f"❌ Minimal execution failed: {e}")
        return False

def main():
    """Main execution function with fallback strategies."""
    print("🌐 SAFE STREAMLIT: Starting...")
    print(f"📁 Working directory: {os.getcwd()}")
    print(f"🐍 Python version: {sys.version}")
    
    # Setup safe environment
    setup_environment()
    
    # Check if app_home.py exists
    if not Path('app_home.py').exists():
        print("❌ app_home.py not found!")
        sys.exit(1)
    
    print("✅ app_home.py found")
    
    # Try different execution strategies
    strategies = [
        ("subprocess", run_streamlit_subprocess),
        ("direct import", run_streamlit_direct),
        ("minimal server", run_streamlit_minimal)
    ]
    
    for strategy_name, strategy_func in strategies:
        print(f"🔄 Trying {strategy_name} strategy...")
        try:
            result = strategy_func()
            if result is not False:
                print(f"✅ {strategy_name} strategy succeeded")
                break
        except Exception as e:
            print(f"❌ {strategy_name} strategy failed: {e}")
            continue
    else:
        print("❌ All strategies failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
