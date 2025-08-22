import streamlit as st
import os
import sys
import time
from dotenv import load_dotenv
from datetime import datetime

# Startup logging
print("=" * 50)
print(f"🚀 Open Notebook Streamlit App Starting...")
print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"🐍 Python Version: {sys.version}")
print(f"📂 Working Directory: {os.getcwd()}")
print("=" * 50)

# Load environment variables
print("📝 Loading environment variables...")
load_dotenv()
print("✅ Environment variables loaded")

# Set page config
print("⚙️ Setting up Streamlit page configuration...")
st.set_page_config(
    page_title="Open Notebook",
    page_icon="📚",
    layout="wide"
)
print("✅ Streamlit page configuration set")

# Initialize session state for startup tracking
if 'app_initialized' not in st.session_state:
    st.session_state.app_initialized = False
    st.session_state.startup_time = datetime.now()

print("🎨 Rendering user interface...")

# Header
st.title("📚 Open Notebook")
st.subheader("Home Assistant Add-on")

# Startup status
if not st.session_state.app_initialized:
    with st.spinner("🔄 Initializing Open Notebook..."):
        time.sleep(1)  # Simulate initialization
        st.session_state.app_initialized = True
    
    startup_duration = (datetime.now() - st.session_state.startup_time).total_seconds()
    st.success(f"✅ Open Notebook initialized successfully in {startup_duration:.2f} seconds!")
    print(f"✅ Application fully initialized in {startup_duration:.2f} seconds")
else:
    st.success("✅ Open Notebook is running successfully!")

# Show startup timestamp
st.info(f"🕐 Application started at: {st.session_state.startup_time.strftime('%Y-%m-%d %H:%M:%S')}")

# Configuration Status
st.subheader("⚙️ Configuration Status")

print("🔍 Checking AI provider configurations...")

col1, col2 = st.columns(2)

with col1:
    st.write("**🤖 AI Providers:**")
    
    # Check AI API keys
    providers_status = {}
    
    openai_key = os.getenv('OPENAI_API_KEY', '')
    anthropic_key = os.getenv('ANTHROPIC_API_KEY', '')
    groq_key = os.getenv('GROQ_API_KEY', '')
    google_key = os.getenv('GOOGLE_API_KEY', '')
    mistral_key = os.getenv('MISTRAL_API_KEY', '')
    deepseek_key = os.getenv('DEEPSEEK_API_KEY', '')
    ollama_url = os.getenv('OLLAMA_BASE_URL', '')
    
    providers_status['OpenAI'] = bool(openai_key)
    providers_status['Anthropic (Claude)'] = bool(anthropic_key)
    providers_status['Groq'] = bool(groq_key)
    providers_status['Google AI'] = bool(google_key)
    providers_status['Mistral AI'] = bool(mistral_key)
    providers_status['DeepSeek'] = bool(deepseek_key)
    providers_status['Ollama'] = bool(ollama_url)
    
    configured_count = sum(providers_status.values())
    
    for provider, configured in providers_status.items():
        if configured:
            st.write(f"✅ {provider}: Configured")
            if provider == 'Ollama' and ollama_url:
                st.write(f"   📍 URL: {ollama_url}")
        else:
            st.write(f"❌ {provider}: Not configured")
    
    print(f"🤖 AI Providers configured: {configured_count}/7")

with col2:
    st.write("**🔧 System Settings:**")
    
    database_url = os.getenv('DATABASE_URL', 'memory')
    debug = os.getenv('DEBUG', 'false')
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    max_file_size = os.getenv('MAX_FILE_SIZE_MB', '50')
    enable_auth = os.getenv('ENABLE_AUTH', 'false')
    
    st.write(f"🗄️ Database: {database_url}")
    st.write(f"🐛 Debug: {debug}")
    st.write(f"📝 Log Level: {log_level}")
    st.write(f"📁 Max File Size: {max_file_size}MB")
    st.write(f"🔐 Authentication: {enable_auth}")
    
    print(f"⚙️ System settings loaded - Debug: {debug}, Log Level: {log_level}")

# AI Configuration Status
ai_configured = configured_count > 0

if not ai_configured:
    st.warning("""
    ⚠️ **No AI providers configured!**
    
    To use Open Notebook, you need to configure at least one AI provider:
    1. Go to **Supervisor → Add-on Store → Open Notebook → Configuration**
    2. Add your API key for at least one provider
    3. Restart the addon
    """)
    print("⚠️ WARNING: No AI providers configured")
else:
    st.success(f"🎉 {configured_count} AI provider(s) configured! Open Notebook is ready to use.")
    print(f"✅ {configured_count} AI provider(s) ready for use")

# System Information
st.subheader("🔧 System Information")
col1, col2 = st.columns(2)

with col1:
    st.write("**📁 Directories:**")
    directories = {
        "Config": "/config/open-notebook",
        "Share": "/share/open-notebook", 
        "App": "/app",
        "Logs": "/app/logs"
    }
    
    for name, path in directories.items():
        if os.path.exists(path):
            st.write(f"✅ {name}: `{path}`")
        else:
            st.write(f"❌ {name}: `{path}` (not found)")

with col2:
    st.write("**✅ Runtime Status:**")
    
    # Check Python
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    st.write(f"🐍 Python: {python_version}")
    
    # Check Streamlit
    try:
        import streamlit as st_check
        st_version = st_check.__version__
        st.write(f"🌊 Streamlit: {st_version}")
    except:
        st.write("❌ Streamlit: Error getting version")
    
    # Check other packages
    try:
        import dotenv
        st.write("✅ python-dotenv: Available")
    except ImportError:
        st.write("❌ python-dotenv: Not available")
    
    # Memory usage (if available)
    try:
        import psutil
        memory = psutil.virtual_memory()
        st.write(f"💾 Memory: {memory.percent}% used")
    except ImportError:
        st.write("💾 Memory: Info not available")

# Test file operations
print("🧪 Testing file system operations...")
try:
    os.makedirs("/config/open-notebook", exist_ok=True)
    os.makedirs("/share/open-notebook", exist_ok=True)
    os.makedirs("/app/logs", exist_ok=True)
    
    # Test write permissions
    test_file = "/config/open-notebook/.test"
    with open(test_file, 'w') as f:
        f.write("test")
    os.remove(test_file)
    
    st.success("✅ File system operations successful")
    print("✅ File system test passed")
except Exception as e:
    st.error(f"❌ File system error: {e}")
    print(f"❌ File system test failed: {e}")

# Configuration Instructions
st.subheader("📝 Configuration Guide")

with st.expander("🔧 How to Configure API Keys"):
    st.write("**Step 1: Go to Addon Configuration**")
    st.write("Navigate to: `Supervisor → Add-on Store → Open Notebook → Configuration`")
    
    st.write("**Step 2: Add API Keys**")
    st.code("""
# Example configuration:
openai_api_key: "sk-your-openai-key-here"
anthropic_api_key: "sk-ant-your-anthropic-key"
groq_api_key: "gsk_your-groq-key"

# Optional settings:
debug: false
log_level: "INFO"
max_file_size: 50
enable_auth: false
""", language="yaml")
    
    st.write("**Step 3: Get API Keys from Providers**")
    providers_links = {
        "OpenAI": "https://platform.openai.com/api-keys",
        "Anthropic": "https://console.anthropic.com/",
        "Groq": "https://console.groq.com/keys",
        "Google AI": "https://makersuite.google.com/app/apikey",
        "Mistral AI": "https://console.mistral.ai/",
        "DeepSeek": "https://platform.deepseek.com/"
    }
    
    for provider, link in providers_links.items():
        st.write(f"- 🔗 [{provider}]({link})")
    
    st.write("**Step 4: Restart Addon**")
    st.write("After adding your API keys, restart the addon to apply the configuration.")

# Future Features
with st.expander("🚀 Roadmap - Coming Soon"):
    st.write("This is the configuration and testing version. The full version will include:")
    
    features = [
        "📄 Document upload and processing (PDF, DOCX, TXT, MD, HTML)",
        "🎙️ Podcast transcription and analysis",
        "💬 Interactive chat with your documents",
        "🔍 Smart search across all content",
        "📚 Notebook organization and management",
        "🔄 Data transformations and insights",
        "📊 Analytics and reporting",
        "🔗 Integration with external sources",
        "🎯 Custom AI workflows",
        "📱 Mobile-optimized interface"
    ]
    
    for feature in features:
        st.write(f"- {feature}")

# Debug Information (only if debug is enabled)
if debug.lower() == 'true':
    st.subheader("🐛 Debug Information")
    
    with st.expander("Environment Variables"):
        env_vars = dict(os.environ)
        for key, value in sorted(env_vars.items()):
            if any(sensitive in key.upper() for sensitive in ['API_KEY', 'PASSWORD', 'SECRET', 'TOKEN']):
                # Hide sensitive information
                if len(value) > 8:
                    display_value = f"{value[:4]}...{value[-4:]}"
                else:
                    display_value = "****"
                st.write(f"`{key}`: {display_value}")
            else:
                st.write(f"`{key}`: {value}")
    
    with st.expander("System Information"):
        st.write(f"**Process ID**: {os.getpid()}")
        st.write(f"**User ID**: {os.getuid()}")
        st.write(f"**Group ID**: {os.getgid()}")
        st.write(f"**Current Directory**: {os.getcwd()}")
        st.write(f"**Python Path**: {sys.executable}")

# Footer
st.markdown("---")
st.markdown("**Open Notebook** - An open source, privacy-focused alternative to Google's Notebook LM")
st.markdown("🏠 Running on Home Assistant | 📚 [Documentation](https://github.com/lfnovo/open-notebook)")

print("✅ User interface rendering completed")
print("🎉 Open Notebook application fully loaded and ready!")
print("=" * 50)
