# Changelog

## [0.3.2] - 2025-08-22

### Added
- Initial release of Open Notebook Home Assistant addon
- Streamlit web interface on port 8501
- FastAPI backend on port 8000
- Support for multiple AI providers (OpenAI, Anthropic, Groq, Google, Mistral, DeepSeek, Ollama)
- Document processing (PDF, DOCX, TXT, MD, HTML)
- Podcast integration with transcription and analysis
- Interactive chat with AI about research materials
- Smart search across all sources
- Note-taking and notebook organization
- Multi-architecture support (amd64, aarch64)
- Complete documentation in English and Portuguese
- Supervisor-managed multi-service architecture
- Integration with Home Assistant directories (/config, /share, /media)
- Authentication and security options
- Health checks and logging

### Technical Details
- Based on open-notebook project v0.3.2
- Uses Alpine Linux base images
- Python 3.11 runtime
- SQLite database support
- Supervisor for process management
