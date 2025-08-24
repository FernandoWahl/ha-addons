#!/usr/bin/env python3
"""
Fallback HTTP server for Open Notebook when Streamlit fails with SIGILL.
This serves a basic web interface that proxies to the API.
"""

import os
import sys
import json
import asyncio
from pathlib import Path
from typing import Dict, Any

try:
    from fastapi import FastAPI, Request, Response
    from fastapi.responses import HTMLResponse, JSONResponse
    from fastapi.staticfiles import StaticFiles
    import uvicorn
    import httpx
except ImportError as e:
    print(f"❌ Missing dependencies: {e}")
    print("📦 Installing required packages...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn", "httpx"])
    from fastapi import FastAPI, Request, Response
    from fastapi.responses import HTMLResponse, JSONResponse
    from fastapi.staticfiles import StaticFiles
    import uvicorn
    import httpx

app = FastAPI(title="Open Notebook Fallback Interface")

# API base URL
API_BASE_URL = "http://localhost:8000"

@app.get("/", response_class=HTMLResponse)
async def home():
    """Serve the main interface."""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Open Notebook - Fallback Interface</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                padding: 30px;
            }
            .header {
                text-align: center;
                margin-bottom: 30px;
                padding-bottom: 20px;
                border-bottom: 2px solid #e0e0e0;
            }
            .header h1 {
                color: #333;
                margin: 0;
                font-size: 2.5em;
            }
            .header p {
                color: #666;
                margin: 10px 0 0 0;
                font-size: 1.1em;
            }
            .status-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            .status-card {
                background: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 6px;
                padding: 20px;
            }
            .status-card h3 {
                margin: 0 0 15px 0;
                color: #495057;
            }
            .status-indicator {
                display: inline-block;
                width: 12px;
                height: 12px;
                border-radius: 50%;
                margin-right: 8px;
            }
            .status-ok { background-color: #28a745; }
            .status-error { background-color: #dc3545; }
            .status-warning { background-color: #ffc107; }
            .api-section {
                margin-top: 30px;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 6px;
            }
            .api-section h3 {
                margin: 0 0 15px 0;
                color: #495057;
            }
            .btn {
                background: #007bff;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                cursor: pointer;
                margin: 5px;
                text-decoration: none;
                display: inline-block;
            }
            .btn:hover {
                background: #0056b3;
            }
            .response-area {
                margin-top: 15px;
                padding: 15px;
                background: white;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                font-family: monospace;
                white-space: pre-wrap;
                max-height: 300px;
                overflow-y: auto;
            }
            .warning-banner {
                background: #fff3cd;
                border: 1px solid #ffeaa7;
                color: #856404;
                padding: 15px;
                border-radius: 6px;
                margin-bottom: 20px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 Open Notebook</h1>
                <p>Fallback Interface - PostgreSQL Compatible Version</p>
            </div>
            
            <div class="warning-banner">
                <strong>⚠️ Fallback Mode:</strong> The main Streamlit interface encountered compatibility issues (SIGILL). 
                This simplified interface provides basic functionality while we resolve the issue.
            </div>
            
            <div class="status-grid">
                <div class="status-card">
                    <h3><span class="status-indicator status-ok"></span>API Server</h3>
                    <p>FastAPI backend is running on port 8000</p>
                    <p><strong>Status:</strong> <span id="api-status">Checking...</span></p>
                </div>
                
                <div class="status-card">
                    <h3><span class="status-indicator status-warning"></span>Database</h3>
                    <p>PostgreSQL connection established</p>
                    <p><strong>Mode:</strong> PostgreSQL Compatible</p>
                </div>
                
                <div class="status-card">
                    <h3><span class="status-indicator status-error"></span>Streamlit UI</h3>
                    <p>Main interface unavailable due to SIGILL error</p>
                    <p><strong>Fallback:</strong> This simplified interface</p>
                </div>
            </div>
            
            <div class="api-section">
                <h3>🔌 API Testing</h3>
                <p>Test the Open Notebook API endpoints:</p>
                
                <button class="btn" onclick="testEndpoint('/health')">Health Check</button>
                <button class="btn" onclick="testEndpoint('/api/models')">List Models</button>
                <button class="btn" onclick="testEndpoint('/api/models/defaults')">Default Models</button>
                <button class="btn" onclick="testEndpoint('/docs')">API Documentation</button>
                
                <div id="response" class="response-area">
                    Click a button above to test API endpoints...
                </div>
            </div>
            
            <div class="api-section">
                <h3>🔗 Direct Links</h3>
                <p>Access Open Notebook services directly:</p>
                <a href="/api/docs" class="btn" target="_blank">📚 API Documentation</a>
                <a href="/api/health" class="btn" target="_blank">💚 Health Check</a>
                <a href="/api/models" class="btn" target="_blank">🤖 Models API</a>
            </div>
        </div>
        
        <script>
            async function testEndpoint(endpoint) {
                const responseArea = document.getElementById('response');
                responseArea.textContent = `Testing ${endpoint}...`;
                
                try {
                    const response = await fetch(`http://localhost:8000${endpoint}`);
                    const data = await response.text();
                    
                    responseArea.textContent = `Status: ${response.status}\\n\\n${data}`;
                } catch (error) {
                    responseArea.textContent = `Error: ${error.message}`;
                }
            }
            
            async function checkApiStatus() {
                try {
                    const response = await fetch('http://localhost:8000/health');
                    document.getElementById('api-status').textContent = response.ok ? 'Online ✅' : 'Error ❌';
                } catch (error) {
                    document.getElementById('api-status').textContent = 'Offline ❌';
                }
            }
            
            // Check API status on load
            checkApiStatus();
            
            // Refresh status every 30 seconds
            setInterval(checkApiStatus, 30000);
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/api/{path:path}")
async def proxy_api(path: str, request: Request):
    """Proxy API requests to the main API server."""
    try:
        async with httpx.AsyncClient() as client:
            url = f"{API_BASE_URL}/api/{path}"
            response = await client.get(url, params=dict(request.query_params))
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Proxy error: {str(e)}"}
        )

@app.get("/health")
async def proxy_health():
    """Proxy health check to the main API server."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_BASE_URL}/health")
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Health check failed: {str(e)}"}
        )

def main():
    """Run the fallback server."""
    print("🌐 FALLBACK SERVER: Starting...")
    print(f"📁 Working directory: {os.getcwd()}")
    print("🔄 This is a fallback interface for when Streamlit fails")
    print("🌐 Fallback UI will be available at: http://0.0.0.0:8502")
    
    # Configure uvicorn
    config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=8502,
        log_level="info",
        access_log=True
    )
    
    server = uvicorn.Server(config)
    server.run()

if __name__ == "__main__":
    main()
