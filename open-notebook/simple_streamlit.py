#!/usr/bin/env python3
"""
Simple Streamlit runner that bypasses streamlit run command
"""

import os
import sys
import subprocess

def main():
    print("🌐 SIMPLE STREAMLIT: Starting...")
    
    # Set working directory
    os.chdir('/app/open-notebook-src')
    print(f"📁 Working directory: {os.getcwd()}")
    
    # Set environment variables
    os.environ['USE_POSTGRESQL'] = 'true'
    os.environ['SKIP_SURREALDB_MIGRATION'] = 'true'
    
    print("🌍 Environment configured for PostgreSQL")
    
    # Try direct Python execution instead of streamlit run
    try:
        print("🚀 Starting Streamlit via direct Python execution...")
        
        # Import and run streamlit directly
        import streamlit.web.cli as stcli
        
        # Set up arguments for streamlit
        sys.argv = [
            "streamlit",
            "run",
            "app_home.py",
            "--server.port=8502",
            "--server.address=0.0.0.0",
            "--server.headless=true",
            "--server.enableCORS=false",
            "--server.enableXsrfProtection=false",
            "--server.runOnSave=false",
            "--browser.gatherUsageStats=false"
        ]
        
        # Run streamlit
        stcli.main()
        
    except Exception as e:
        print(f"❌ Direct execution failed: {e}")
        
        # Fallback: try subprocess with different approach
        try:
            print("🔄 Trying subprocess approach...")
            
            cmd = [
                sys.executable, 
                "-c", 
                """
import streamlit.web.cli as stcli
import sys
sys.argv = ['streamlit', 'run', 'app_home.py', '--server.port=8502', '--server.address=0.0.0.0', '--server.headless=true', '--server.enableCORS=false', '--server.enableXsrfProtection=false']
stcli.main()
"""
            ]
            
            subprocess.run(cmd, cwd='/app/open-notebook-src')
            
        except Exception as e2:
            print(f"❌ Subprocess approach failed: {e2}")
            
            # Final fallback: basic streamlit
            try:
                print("🔄 Trying basic streamlit command...")
                subprocess.run([
                    sys.executable, "-m", "streamlit", "run", "app_home.py",
                    "--server.port=8502"
                ], cwd='/app/open-notebook-src')
            except Exception as e3:
                print(f"❌ All approaches failed: {e3}")
                return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
