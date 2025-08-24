#!/usr/bin/env python3
"""
Wait for API to be ready before starting Streamlit
"""

import time
import requests
import sys
import os

def wait_for_api(max_attempts=30, delay=2):
    """Wait for API to be ready"""
    print("🔍 Waiting for API to be ready...")
    print(f"📊 Max attempts: {max_attempts}, Delay: {delay}s")
    
    for attempt in range(max_attempts):
        try:
            # Try to connect to the API health endpoint
            print(f"⏳ Attempt {attempt + 1}/{max_attempts}: Testing http://localhost:8000/health")
            response = requests.get("http://localhost:8000/health", timeout=5)
            print(f"📊 Health endpoint response: {response.status_code}")
            if response.status_code == 200:
                print("✅ API health check passed!")
                return True
        except requests.exceptions.RequestException as e:
            print(f"❌ Health endpoint failed: {e}")
        
        # Try basic connection
        try:
            print(f"⏳ Attempt {attempt + 1}/{max_attempts}: Testing http://localhost:8000/")
            response = requests.get("http://localhost:8000/", timeout=5)
            print(f"📊 Root endpoint response: {response.status_code}")
            if response.status_code in [200, 404, 422]:  # 422 is also OK for FastAPI
                print("✅ API is responding!")
                return True
        except requests.exceptions.RequestException as e:
            print(f"❌ Root endpoint failed: {e}")
        
        # Try docs endpoint
        try:
            print(f"⏳ Attempt {attempt + 1}/{max_attempts}: Testing http://localhost:8000/docs")
            response = requests.get("http://localhost:8000/docs", timeout=5)
            print(f"📊 Docs endpoint response: {response.status_code}")
            if response.status_code == 200:
                print("✅ API docs accessible!")
                return True
        except requests.exceptions.RequestException as e:
            print(f"❌ Docs endpoint failed: {e}")
        
        print(f"⏳ API not ready yet (attempt {attempt + 1}/{max_attempts})")
        if attempt < max_attempts - 1:
            print(f"💤 Sleeping {delay}s before next attempt...")
            time.sleep(delay)
    
    print("❌ API failed to start within timeout")
    print("🔍 Checking if API process is running...")
    
    # Check if API process exists
    try:
        import subprocess
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        if 'run_api.py' in result.stdout:
            print("✅ API process is running")
        else:
            print("❌ API process not found")
        
        # Show API logs if available
        if os.path.exists('/app/logs/api_error.log'):
            print("📋 API Error Log (last 10 lines):")
            with open('/app/logs/api_error.log', 'r') as f:
                lines = f.readlines()
                for line in lines[-10:]:
                    print(f"  {line.strip()}")
        
        if os.path.exists('/app/logs/api_output.log'):
            print("📋 API Output Log (last 10 lines):")
            with open('/app/logs/api_output.log', 'r') as f:
                lines = f.readlines()
                for line in lines[-10:]:
                    print(f"  {line.strip()}")
                    
    except Exception as e:
        print(f"❌ Error checking API process: {e}")
    
    return False

if __name__ == "__main__":
    print("🚀 API Wait Script Starting...")
    print(f"🐍 Python version: {sys.version}")
    print(f"📁 Working directory: {os.getcwd()}")
    print(f"🌍 Environment variables:")
    for key in ['USE_POSTGRESQL', 'DATABASE_URL', 'PYTHONPATH']:
        print(f"  {key}: {os.getenv(key, 'Not set')}")
    
    if wait_for_api():
        print("🚀 API is ready - Starting Streamlit...")
        sys.exit(0)
    else:
        print("❌ API startup failed - Exiting")
        sys.exit(1)
