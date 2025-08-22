import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="Open Notebook",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Open Notebook")
st.subheader("Home Assistant Add-on")

st.success("✅ Open Notebook is running successfully!")

# Configuration Status
st.subheader("⚙️ Configuration Status")

col1, col2 = st.columns(2)

with col1:
    st.write("**🤖 AI Providers:**")
    
    # Check AI API keys
    openai_key = os.getenv('OPENAI_API_KEY', '')
    anthropic_key = os.getenv('ANTHROPIC_API_KEY', '')
    groq_key = os.getenv('GROQ_API_KEY', '')
    google_key = os.getenv('GOOGLE_API_KEY', '')
    mistral_key = os.getenv('MISTRAL_API_KEY', '')
    deepseek_key = os.getenv('DEEPSEEK_API_KEY', '')
    ollama_url = os.getenv('OLLAMA_BASE_URL', '')
    
    if openai_key:
        st.write("✅ OpenAI: Configured")
    else:
        st.write("❌ OpenAI: Not configured")
        
    if anthropic_key:
        st.write("✅ Anthropic (Claude): Configured")
    else:
        st.write("❌ Anthropic (Claude): Not configured")
        
    if groq_key:
        st.write("✅ Groq: Configured")
    else:
        st.write("❌ Groq: Not configured")
        
    if google_key:
        st.write("✅ Google AI: Configured")
    else:
        st.write("❌ Google AI: Not configured")
        
    if mistral_key:
        st.write("✅ Mistral AI: Configured")
    else:
        st.write("❌ Mistral AI: Not configured")
        
    if deepseek_key:
        st.write("✅ DeepSeek: Configured")
    else:
        st.write("❌ DeepSeek: Not configured")
        
    if ollama_url:
        st.write(f"✅ Ollama: {ollama_url}")
    else:
        st.write("❌ Ollama: Not configured")

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

# Check if any AI provider is configured
ai_configured = any([openai_key, anthropic_key, groq_key, google_key, mistral_key, deepseek_key, ollama_url])

if not ai_configured:
    st.warning("""
    ⚠️ **No AI providers configured!**
    
    To use Open Notebook, you need to configure at least one AI provider:
    1. Go to **Supervisor → Add-on Store → Open Notebook → Configuration**
    2. Add your API key for at least one provider
    3. Restart the addon
    """)
else:
    st.success("🎉 AI providers configured! Open Notebook is ready to use.")

# System Information
st.subheader("🔧 System Information")
col1, col2 = st.columns(2)

with col1:
    st.write("**📁 Directories:**")
    st.write(f"- Config: `/config/open-notebook`")
    st.write(f"- Share: `/share/open-notebook`")
    st.write(f"- App: `/app`")

with col2:
    st.write("**✅ Status:**")
    st.write("- ✅ Streamlit: Running")
    st.write("- ✅ Python: Available")
    st.write("- ✅ File System: Accessible")

# Test file operations
try:
    os.makedirs("/config/open-notebook", exist_ok=True)
    os.makedirs("/share/open-notebook", exist_ok=True)
    st.success("✅ Directory creation successful")
except Exception as e:
    st.error(f"❌ Directory creation failed: {e}")

# Configuration Instructions
st.subheader("📝 How to Configure")

st.write("**Step 1: Add API Keys**")
st.write("Go to the addon configuration and add your API keys:")

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

st.write("**Step 2: Get API Keys**")
st.write("Get your API keys from these providers:")
st.write("- 🔗 [OpenAI](https://platform.openai.com/api-keys)")
st.write("- 🔗 [Anthropic](https://console.anthropic.com/)")
st.write("- 🔗 [Groq](https://console.groq.com/keys)")
st.write("- 🔗 [Google AI](https://makersuite.google.com/app/apikey)")
st.write("- 🔗 [Mistral AI](https://console.mistral.ai/)")
st.write("- 🔗 [DeepSeek](https://platform.deepseek.com/)")

st.write("**Step 3: Restart Addon**")
st.write("After adding your API keys, restart the addon to apply the configuration.")

# Future Features
st.subheader("🚀 Coming Soon")
st.write("This is the basic version. The full version will include:")
st.write("- 📄 Document upload and processing")
st.write("- 🎙️ Podcast transcription and analysis")
st.write("- 💬 Interactive chat with your documents")
st.write("- 🔍 Smart search across all content")
st.write("- 📚 Notebook organization")
st.write("- 🔄 Data transformations")

# Environment Variables Debug (only if debug is enabled)
if debug.lower() == 'true':
    st.subheader("🐛 Debug Information")
    with st.expander("Environment Variables"):
        env_vars = dict(os.environ)
        for key, value in sorted(env_vars.items()):
            if 'API_KEY' in key or 'PASSWORD' in key:
                # Hide sensitive information
                display_value = f"{'*' * (len(value) - 4)}{value[-4:]}" if len(value) > 4 else "****"
                st.write(f"{key}: {display_value}")
            else:
                st.write(f"{key}: {value}")
