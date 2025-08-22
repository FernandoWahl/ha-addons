#!/usr/bin/env python3

import os
import sys
import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import logging
from dotenv import load_dotenv
import json
import aiofiles
from pathlib import Path

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Open Notebook API",
    description="Backend API for Open Notebook - AI-powered research assistant",
    version="0.5.2"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class ChatMessage(BaseModel):
    message: str
    provider: Optional[str] = "openai"

class ChatResponse(BaseModel):
    response: str
    provider: str
    timestamp: str

class DocumentInfo(BaseModel):
    filename: str
    size: int
    type: str
    uploaded_at: str

class NotebookCreate(BaseModel):
    name: str
    description: Optional[str] = ""

class NotebookInfo(BaseModel):
    id: str
    name: str
    description: str
    created_at: str
    document_count: int

# Global variables
UPLOAD_DIR = Path("/config/open-notebook/uploads")
NOTEBOOKS_DIR = Path("/config/open-notebook/notebooks")
DATA_DIR = Path("/config/open-notebook/data")

# Ensure directories exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
NOTEBOOKS_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Open Notebook API starting up...")
    logger.info(f"📁 Upload directory: {UPLOAD_DIR}")
    logger.info(f"📚 Notebooks directory: {NOTEBOOKS_DIR}")
    logger.info(f"🗄️ Data directory: {DATA_DIR}")
    
    # Check AI providers
    providers = {
        "OpenAI": os.getenv('OPENAI_API_KEY', ''),
        "Anthropic": os.getenv('ANTHROPIC_API_KEY', ''),
        "Groq": os.getenv('GROQ_API_KEY', ''),
        "Google": os.getenv('GOOGLE_API_KEY', ''),
        "Mistral": os.getenv('MISTRAL_API_KEY', ''),
        "DeepSeek": os.getenv('DEEPSEEK_API_KEY', ''),
    }
    
    configured_providers = [name for name, key in providers.items() if key]
    logger.info(f"🤖 Configured AI providers: {configured_providers}")
    
    logger.info("✅ Open Notebook API ready!")

@app.get("/")
async def root():
    return {
        "message": "Open Notebook API",
        "version": "0.5.2",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "chat": "/chat",
            "upload": "/upload",
            "documents": "/documents",
            "notebooks": "/notebooks"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "0.5.2",
        "timestamp": "2025-08-22T17:44:00Z",
        "services": {
            "api": "running",
            "storage": "available",
            "ai_providers": "configured"
        }
    }

@app.post("/chat", response_model=ChatResponse)
async def chat_with_ai(message: ChatMessage):
    """Chat with AI providers"""
    try:
        # Get API key for selected provider
        provider = message.provider.lower()
        api_key = ""
        
        if provider == "openai":
            api_key = os.getenv('OPENAI_API_KEY', '')
        elif provider == "anthropic":
            api_key = os.getenv('ANTHROPIC_API_KEY', '')
        elif provider == "groq":
            api_key = os.getenv('GROQ_API_KEY', '')
        elif provider == "google":
            api_key = os.getenv('GOOGLE_API_KEY', '')
        elif provider == "mistral":
            api_key = os.getenv('MISTRAL_API_KEY', '')
        elif provider == "deepseek":
            api_key = os.getenv('DEEPSEEK_API_KEY', '')
        
        if not api_key:
            raise HTTPException(
                status_code=400, 
                detail=f"API key not configured for provider: {provider}"
            )
        
        # For now, return a mock response
        # TODO: Implement actual AI provider integration
        response_text = f"Hello! I received your message: '{message.message}'. I'm ready to help with your research using {provider.title()}. Please note that full AI integration is coming soon!"
        
        return ChatResponse(
            response=response_text,
            provider=provider,
            timestamp="2025-08-22T17:44:00Z"
        )
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload and process documents"""
    try:
        # Validate file type
        allowed_types = ['.pdf', '.docx', '.txt', '.md', '.html']
        file_ext = Path(file.filename).suffix.lower()
        
        if file_ext not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail=f"File type {file_ext} not allowed. Allowed types: {allowed_types}"
            )
        
        # Save file
        file_path = UPLOAD_DIR / file.filename
        
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # Create document info
        doc_info = {
            "filename": file.filename,
            "size": len(content),
            "type": file_ext,
            "uploaded_at": "2025-08-22T17:44:00Z",
            "path": str(file_path)
        }
        
        logger.info(f"📄 Uploaded document: {file.filename} ({len(content)} bytes)")
        
        return JSONResponse(content={
            "message": "Document uploaded successfully",
            "document": doc_info
        })
        
    except Exception as e:
        logger.error(f"Upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documents", response_model=List[DocumentInfo])
async def list_documents():
    """List uploaded documents"""
    try:
        documents = []
        
        for file_path in UPLOAD_DIR.glob("*"):
            if file_path.is_file():
                stat = file_path.stat()
                documents.append(DocumentInfo(
                    filename=file_path.name,
                    size=stat.st_size,
                    type=file_path.suffix.lower(),
                    uploaded_at="2025-08-22T17:44:00Z"
                ))
        
        return documents
        
    except Exception as e:
        logger.error(f"List documents error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/notebooks", response_model=NotebookInfo)
async def create_notebook(notebook: NotebookCreate):
    """Create a new notebook"""
    try:
        notebook_id = f"notebook_{len(list(NOTEBOOKS_DIR.glob('*.json'))) + 1}"
        notebook_file = NOTEBOOKS_DIR / f"{notebook_id}.json"
        
        notebook_data = {
            "id": notebook_id,
            "name": notebook.name,
            "description": notebook.description,
            "created_at": "2025-08-22T17:44:00Z",
            "documents": [],
            "notes": []
        }
        
        async with aiofiles.open(notebook_file, 'w') as f:
            await f.write(json.dumps(notebook_data, indent=2))
        
        logger.info(f"📚 Created notebook: {notebook.name}")
        
        return NotebookInfo(
            id=notebook_id,
            name=notebook.name,
            description=notebook.description,
            created_at="2025-08-22T17:44:00Z",
            document_count=0
        )
        
    except Exception as e:
        logger.error(f"Create notebook error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/notebooks", response_model=List[NotebookInfo])
async def list_notebooks():
    """List all notebooks"""
    try:
        notebooks = []
        
        for notebook_file in NOTEBOOKS_DIR.glob("*.json"):
            async with aiofiles.open(notebook_file, 'r') as f:
                content = await f.read()
                notebook_data = json.loads(content)
                
                notebooks.append(NotebookInfo(
                    id=notebook_data["id"],
                    name=notebook_data["name"],
                    description=notebook_data["description"],
                    created_at=notebook_data["created_at"],
                    document_count=len(notebook_data.get("documents", []))
                ))
        
        return notebooks
        
    except Exception as e:
        logger.error(f"List notebooks error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/config")
async def get_config():
    """Get current configuration"""
    try:
        providers = {
            "openai": bool(os.getenv('OPENAI_API_KEY', '')),
            "anthropic": bool(os.getenv('ANTHROPIC_API_KEY', '')),
            "groq": bool(os.getenv('GROQ_API_KEY', '')),
            "google": bool(os.getenv('GOOGLE_API_KEY', '')),
            "mistral": bool(os.getenv('MISTRAL_API_KEY', '')),
            "deepseek": bool(os.getenv('DEEPSEEK_API_KEY', '')),
        }
        
        return {
            "providers": providers,
            "configured_count": sum(providers.values()),
            "debug": os.getenv('DEBUG', 'false').lower() == 'true',
            "max_file_size": int(os.getenv('MAX_FILE_SIZE_MB', '50')),
            "data_dir": str(DATA_DIR),
            "upload_dir": str(UPLOAD_DIR),
            "notebooks_dir": str(NOTEBOOKS_DIR)
        }
        
    except Exception as e:
        logger.error(f"Get config error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Get configuration
    host = os.getenv('FASTAPI_SERVER_ADDRESS', '0.0.0.0')
    port = int(os.getenv('FASTAPI_SERVER_PORT', '8000'))
    debug = os.getenv('DEBUG', 'false').lower() == 'true'
    
    logger.info(f"🚀 Starting FastAPI server on {host}:{port}")
    logger.info(f"🐛 Debug mode: {debug}")
    
    # Run the server
    uvicorn.run(
        "run_api:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info"
    )
