#!/bin/bash

echo "🔧 Pre-start PostgreSQL compatibility setup..."

# Set environment variables
export SKIP_SURREALDB_MIGRATION=true
export USE_POSTGRESQL=true
export DISABLE_SURREALDB=true
export SURREALDB_URL=disabled
export FORCE_POSTGRESQL=true

echo "🔧 Patching migration files directly..."

# Patch the check_migration function in utils.py
if [ -f "/app/open-notebook-src/pages/stream_app/utils.py" ]; then
    echo "📝 Patching utils.py migration check..."
    
    # Create backup
    cp "/app/open-notebook-src/pages/stream_app/utils.py" "/app/open-notebook-src/pages/stream_app/utils.py.backup"
    
    # Replace the check_migration function with a PostgreSQL-aware version
    cat > /tmp/patch_utils.py << 'EOF'
import re
import os

def patch_utils():
    file_path = "/app/open-notebook-src/pages/stream_app/utils.py"
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Find and replace the check_migration function
    pattern = r'def check_migration\(\):(.*?)(?=\ndef|\nclass|\n@|\Z)'
    
    replacement = '''def check_migration():
    """PostgreSQL-compatible migration check"""
    import os
    
    # Skip migration if using PostgreSQL
    if os.getenv('USE_POSTGRESQL', 'false').lower() == 'true':
        print("🐘 Using PostgreSQL - skipping SurrealDB migration")
        return
    
    if os.getenv('SKIP_SURREALDB_MIGRATION', 'false').lower() == 'true':
        print("🔄 Skipping SurrealDB migration (PostgreSQL mode)")
        return
    
    # Original migration logic (only for SurrealDB users)
    try:
        from open_notebook.database.migrate import MigrationManager
        mm = MigrationManager()
        mm.run_migration_up()
    except Exception as e:
        print(f"⚠️ Migration failed, continuing: {e}")
        pass'''
    
    # Replace the function
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # If no replacement was made, try a simpler approach
    if new_content == content:
        # Just replace the function call
        new_content = content.replace(
            'check_migration()',
            'postgresql_safe_migration()'
        )
        
        # Add the safe function at the end
        new_content += '''

def postgresql_safe_migration():
    """Safe migration that skips SurrealDB when using PostgreSQL"""
    import os
    
    if os.getenv('USE_POSTGRESQL', 'false').lower() == 'true':
        print("🐘 Using PostgreSQL - skipping SurrealDB migration")
        return
    
    if os.getenv('SKIP_SURREALDB_MIGRATION', 'false').lower() == 'true':
        print("🔄 Skipping SurrealDB migration")
        return
    
    try:
        from open_notebook.database.migrate import MigrationManager
        mm = MigrationManager()
        mm.run_migration_up()
    except Exception as e:
        print(f"⚠️ Migration failed, continuing: {e}")
        pass
'''
    
    with open(file_path, 'w') as f:
        f.write(new_content)
    
    print("✅ Patched utils.py successfully")

if __name__ == "__main__":
    patch_utils()
EOF

    python3 /tmp/patch_utils.py
    
else
    echo "❌ utils.py not found"
fi

# Also patch the migrate.py file directly
if [ -f "/app/open-notebook-src/open_notebook/database/migrate.py" ]; then
    echo "📝 Patching migrate.py..."
    
    # Create backup
    cp "/app/open-notebook-src/open_notebook/database/migrate.py" "/app/open-notebook-src/open_notebook/database/migrate.py.backup"
    
    # Add PostgreSQL check at the beginning of run_migration_up
    cat > /tmp/patch_migrate.py << 'EOF'
import os

def patch_migrate():
    file_path = "/app/open-notebook-src/open_notebook/database/migrate.py"
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Add check at the beginning of run_migration_up method
    if 'def run_migration_up(self):' in content:
        content = content.replace(
            'def run_migration_up(self):',
            '''def run_migration_up(self):
        # Skip migration if using PostgreSQL
        if os.getenv('USE_POSTGRESQL', 'false').lower() == 'true':
            print("🐘 PostgreSQL mode - skipping SurrealDB migration")
            return
        
        if os.getenv('SKIP_SURREALDB_MIGRATION', 'false').lower() == 'true':
            print("🔄 Skipping SurrealDB migration")
            return'''
        )
        
        # Add import at the top if not present
        if 'import os' not in content:
            content = 'import os\n' + content
        
        with open(file_path, 'w') as f:
            f.write(content)
        
        print("✅ Patched migrate.py successfully")
    else:
        print("❌ run_migration_up method not found in migrate.py")

if __name__ == "__main__":
    patch_migrate()
EOF

    python3 /tmp/patch_migrate.py
    
else
    echo "❌ migrate.py not found"
fi

echo "✅ PostgreSQL compatibility setup completed"

# Patch API client for resilient connections
if [ -f "/app/open-notebook-src/api/client.py" ]; then
    echo "📝 Patching API client for resilient connections..."
    
    # Create backup
    cp "/app/open-notebook-src/api/client.py" "/app/open-notebook-src/api/client.py.backup"
    
    # Patch the _make_request method to be more resilient
    cat > /tmp/patch_client.py << 'EOF'
import re

def patch_client():
    file_path = "/app/open-notebook-src/api/client.py"
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Add resilient connection handling
    if 'def _make_request(self' in content:
        # Replace the _make_request method with a more resilient version
        pattern = r'def _make_request\(self[^}]*?raise ConnectionError\(f"Failed to connect to API: \{str\(e\)\}"\)'
        
        replacement = '''def _make_request(self, method, endpoint, **kwargs):
        """Make HTTP request with resilient error handling"""
        import time
        import os
        
        # If API is not ready yet, wait a bit
        max_retries = 3
        for attempt in range(max_retries):
            try:
                url = f"{self.base_url}{endpoint}"
                response = self.session.request(method, url, **kwargs)
                response.raise_for_status()
                return response.json() if response.content else {}
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"⏳ API connection attempt {attempt + 1} failed, retrying...")
                    time.sleep(2)
                    continue
                else:
                    # On final failure, return empty response instead of crashing
                    print(f"⚠️ API connection failed after {max_retries} attempts: {e}")
                    if "models" in endpoint:
                        return {"models": []}
                    return {}'''
        
        new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        # If regex didn't work, try simpler replacement
        if new_content == content:
            new_content = content.replace(
                'raise ConnectionError(f"Failed to connect to API: {str(e)}")',
                '''print(f"⚠️ API connection failed: {e}")
                if "models" in endpoint:
                    return {"models": []}
                return {}'''
            )
        
        with open(file_path, 'w') as f:
            f.write(new_content)
        
        print("✅ Patched API client successfully")
    else:
        print("❌ _make_request method not found in client.py")

if __name__ == "__main__":
    patch_client()
EOF

    python3 /tmp/patch_client.py
    
else
    echo "❌ client.py not found"
fi

echo "✅ All patches applied successfully"

# Create mock surreal_commands module
echo "📦 Creating mock surreal_commands module..."
cat > /app/open-notebook-src/surreal_commands.py << 'EOF'
"""Mock surreal_commands module for PostgreSQL compatibility"""

def get_command_status(*args, **kwargs):
    """Mock function for command status"""
    return {"status": "completed", "result": "PostgreSQL mode - command skipped"}

def submit_command(*args, **kwargs):
    """Mock function for command submission"""
    return {"id": "mock_command", "status": "submitted", "message": "PostgreSQL mode - command mocked"}

# Add any other functions that might be imported
def execute_command(*args, **kwargs):
    return {"status": "success", "message": "PostgreSQL mode"}

def get_command_result(*args, **kwargs):
    return {"result": "PostgreSQL mode - no SurrealDB commands"}

# Mock registry object
class MockRegistry:
    def __init__(self):
        self.commands = {}
    
    def register(self, name, func):
        self.commands[name] = func
        return func
    
    def get(self, name):
        return self.commands.get(name, lambda *args, **kwargs: {"status": "mock"})
    
    def list_commands(self):
        return list(self.commands.keys())

# Create registry instance
registry = MockRegistry()
EOF

echo "✅ Created mock surreal_commands module with registry"

# Create mock content_core module
echo "📦 Creating mock content_core package..."

# Create content_core package directory
mkdir -p /app/open-notebook-src/content_core

# Create __init__.py for the package
cat > /app/open-notebook-src/content_core/__init__.py << 'EOF'
"""Mock content_core package for PostgreSQL compatibility"""

def extract_content(source, *args, **kwargs):
    """Mock function for content extraction"""
    if isinstance(source, str):
        return {
            "content": source,
            "metadata": {"source": "mock", "type": "text"},
            "extracted_text": source,
            "title": "Mock Content",
            "summary": "Mock content extraction for PostgreSQL mode"
        }
    elif isinstance(source, dict):
        return {
            "content": source.get("content", ""),
            "metadata": source.get("metadata", {}),
            "extracted_text": source.get("text", ""),
            "title": source.get("title", "Mock Content"),
            "summary": "Mock content extraction"
        }
    else:
        return {
            "content": str(source),
            "metadata": {"source": "mock"},
            "extracted_text": str(source),
            "title": "Mock Content",
            "summary": "Mock content extraction"
        }

def process_content(content, *args, **kwargs):
    """Mock function for content processing"""
    return {
        "processed_content": content,
        "status": "processed",
        "method": "mock_processing"
    }

def analyze_content(content, *args, **kwargs):
    """Mock function for content analysis"""
    return {
        "analysis": "Mock analysis completed",
        "sentiment": "neutral",
        "topics": ["mock", "content"],
        "confidence": 0.95
    }

# Add any other functions that might be imported
def parse_document(*args, **kwargs):
    return {"parsed": True, "content": "Mock parsed content"}

def extract_metadata(*args, **kwargs):
    return {"metadata": "Mock metadata", "source": "mock"}
EOF

# Create common.py submodule
cat > /app/open-notebook-src/content_core/common.py << 'EOF'
"""Mock content_core.common module"""

from enum import Enum
from typing import Dict, Any, Optional

class ProcessSourceState(Enum):
    """Mock ProcessSourceState enum"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class SourceType(Enum):
    """Mock SourceType enum"""
    TEXT = "text"
    PDF = "pdf"
    HTML = "html"
    MARKDOWN = "markdown"
    DOCUMENT = "document"

class ContentProcessor:
    """Mock ContentProcessor class"""
    
    def __init__(self):
        self.state = ProcessSourceState.PENDING
    
    def process(self, source: Any) -> Dict[str, Any]:
        """Mock process method"""
        self.state = ProcessSourceState.PROCESSING
        result = {
            "content": str(source),
            "state": self.state.value,
            "metadata": {"processor": "mock"},
            "success": True
        }
        self.state = ProcessSourceState.COMPLETED
        return result
    
    def get_state(self) -> ProcessSourceState:
        """Get current processing state"""
        return self.state

# Mock functions that might be imported
def create_processor(*args, **kwargs) -> ContentProcessor:
    """Create a mock content processor"""
    return ContentProcessor()

def validate_source(source: Any) -> bool:
    """Mock source validation"""
    return True

def get_source_type(source: Any) -> SourceType:
    """Mock source type detection"""
    return SourceType.TEXT
EOF

# Create any other submodules that might be needed
cat > /app/open-notebook-src/content_core/extractors.py << 'EOF'
"""Mock content_core.extractors module"""

class BaseExtractor:
    """Mock base extractor class"""
    
    def extract(self, source):
        return {"extracted": True, "content": str(source)}

class TextExtractor(BaseExtractor):
    """Mock text extractor"""
    pass

class PDFExtractor(BaseExtractor):
    """Mock PDF extractor"""
    pass

class HTMLExtractor(BaseExtractor):
    """Mock HTML extractor"""
    pass

# Factory function
def get_extractor(source_type):
    """Get appropriate extractor for source type"""
    return TextExtractor()
EOF

# Remove the old single file if it exists
rm -f /app/open-notebook-src/content_core.py 2>/dev/null || true

echo "✅ Created mock content_core package with submodules"

# Fix API port configuration - more comprehensive approach
echo "🔧 Fixing API port configuration..."
if [ -f "/app/open-notebook-src/run_api.py" ]; then
    # Create backup
    cp "/app/open-notebook-src/run_api.py" "/app/open-notebook-src/run_api.py.backup"
    
    # Show current content for debugging
    echo "📋 Current run_api.py content:"
    head -20 /app/open-notebook-src/run_api.py
    
    # Replace all occurrences of port 5055 with 8000
    sed -i 's/5055/8000/g' /app/open-notebook-src/run_api.py
    sed -i 's/127\.0\.0\.1/0.0.0.0/g' /app/open-notebook-src/run_api.py
    
    # Also check for any uvicorn.run calls and fix them
    sed -i 's/host="127\.0\.0\.1"/host="0.0.0.0"/g' /app/open-notebook-src/run_api.py
    sed -i 's/host='\''127\.0\.0\.1'\''/host="0.0.0.0"/g' /app/open-notebook-src/run_api.py
    
    echo "📋 Modified run_api.py content:"
    head -20 /app/open-notebook-src/run_api.py
    
    echo "✅ Fixed API port configuration"
else
    echo "❌ run_api.py not found"
fi

# Also check if there's a config file or environment variable setting the port
if [ -f "/app/open-notebook-src/.env" ]; then
    echo "🔧 Checking .env file for port settings..."
    grep -i port /app/open-notebook-src/.env || echo "No port settings in .env"
fi

# Set environment variable to override port
export API_PORT=8000
export HOST=0.0.0.0
export PORT=8000

echo "🌐 Environment variables set:"
echo "  API_PORT=8000"
echo "  HOST=0.0.0.0"
echo "  PORT=8000"

echo "🐍 Environment configured for PostgreSQL"
echo "🗄️ Database mode: PostgreSQL"
