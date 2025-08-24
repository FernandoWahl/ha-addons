#!/usr/bin/env python3
"""
Wait for API to be ready before starting Streamlit
"""

import time
import requests
import sys

def wait_for_api(max_attempts=30, delay=2):
    """Wait for API to be ready"""
    print("🔍 Waiting for API to be ready...")
    
    for attempt in range(max_attempts):
        try:
            # Try to connect to the API health endpoint
            response = requests.get("http://localhost:8000/health", timeout=5)
            if response.status_code == 200:
                print("✅ API is ready!")
                return True
        except requests.exceptions.RequestException:
            pass
        
        # Try basic connection
        try:
            response = requests.get("http://localhost:8000/", timeout=5)
            if response.status_code in [200, 404]:  # 404 is OK, means server is running
                print("✅ API is responding!")
                return True
        except requests.exceptions.RequestException:
            pass
        
        print(f"⏳ API not ready yet (attempt {attempt + 1}/{max_attempts})")
        time.sleep(delay)
    
    print("❌ API failed to start within timeout")
    return False

if __name__ == "__main__":
    if wait_for_api():
        print("🚀 Starting Streamlit...")
        sys.exit(0)
    else:
        print("❌ API startup failed")
        sys.exit(1)
