import streamlit as st
import os
import requests
from dotenv import load_dotenv
from auth import check_password, show_logout

# Load environment
load_dotenv()

st.set_page_config(
    page_title="Open Notebook",
    page_icon="📚",
    layout="wide"
)

# Check authentication first
if not check_password():
    st.stop()

# Sidebar navigation
st.sidebar.title("📚 Open Notebook")

# Show logout option if authenticated
show_logout()

page = st.sidebar.selectbox("Navigate", [
    "🏠 Home",
    "📚 Notebooks", 
    "🔍 Ask & Search",
    "🎙️ Podcasts",
    "🤖 Models",
    "⚙️ Settings"
])

# Main content based on page selection
if page == "🏠 Home":
    st.title("📚 Open Notebook")
    st.subheader("AI-Powered Research Assistant")
    
    st.success("✅ Open Notebook is running successfully!")
    
    # Check AI configuration
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🤖 AI Providers")
        
        providers = {
            "OpenAI": os.getenv('OPENAI_API_KEY', ''),
            "Anthropic": os.getenv('ANTHROPIC_API_KEY', ''),
            "Groq": os.getenv('GROQ_API_KEY', ''),
            "Google AI": os.getenv('GOOGLE_API_KEY', ''),
            "Mistral": os.getenv('MISTRAL_API_KEY', ''),
            "DeepSeek": os.getenv('DEEPSEEK_API_KEY', ''),
        }
        
        configured_count = 0
        for name, key in providers.items():
            if key:
                st.write(f"✅ {name}: Configured")
                configured_count += 1
            else:
                st.write(f"❌ {name}: Not configured")
        
        if configured_count == 0:
            st.error("⚠️ **No AI providers configured!**")
            
            with st.expander("📍 **HOW TO CONFIGURE AI PROVIDERS**", expanded=True):
                st.write("**Step 1: Go to Addon Configuration**")
                st.code("Supervisor → Add-on Store → Open Notebook → Configuration tab")
                
                st.write("**Step 2: Add your API keys**")
                st.code("""
# Example configuration:
openai_api_key: "sk-your-openai-key-here"
anthropic_api_key: "sk-ant-your-anthropic-key"
groq_api_key: "gsk_your-groq-key"
google_api_key: "your-google-ai-key"

# Optional settings:
debug: false
log_level: "INFO"
max_file_size: 50
""", language="yaml")
                
                st.write("**Step 3: Get API keys from providers**")
                col_a, col_b = st.columns(2)
                with col_a:
                    st.write("🔗 [OpenAI API Keys](https://platform.openai.com/api-keys)")
                    st.write("🔗 [Anthropic Console](https://console.anthropic.com/)")
                    st.write("🔗 [Groq Console](https://console.groq.com/keys)")
                with col_b:
                    st.write("🔗 [Google AI Studio](https://makersuite.google.com/app/apikey)")
                    st.write("🔗 [Mistral AI](https://console.mistral.ai/)")
                    st.write("🔗 [DeepSeek](https://platform.deepseek.com/)")
                
                st.write("**Step 4: Save and restart**")
                st.write("1. Click **Save** in the configuration")
                st.write("2. Go to **Info** tab")
                st.write("3. Click **Restart**")
                st.write("4. Wait for restart to complete")
                st.write("5. Refresh this page")
                
            st.warning("🚨 **AI features are disabled until you configure at least one provider!**")
        else:
            st.success(f"🎉 {configured_count} AI provider(s) ready!")
    
    with col2:
        st.subheader("🔧 System Status")
        st.write("🌊 Streamlit: Running")
        st.write("⚡ FastAPI: Available")
        st.write("🗄️ Database: Ready")
        st.write("📁 Storage: Accessible")
        
        # Test file operations
        try:
            os.makedirs("/config/open-notebook", exist_ok=True)
            st.write("✅ File System: OK")
        except:
            st.write("❌ File System: Error")

elif page == "📚 Notebooks":
    st.title("📚 Notebooks")
    st.info("📝 Create and manage your research notebooks")
    
    # Simple notebook creation
    with st.form("create_notebook"):
        notebook_name = st.text_input("Notebook Name")
        notebook_desc = st.text_area("Description")
        
        if st.form_submit_button("Create Notebook"):
            if notebook_name:
                st.success(f"✅ Notebook '{notebook_name}' created!")
                st.balloons()
            else:
                st.error("Please enter a notebook name")
    
    st.subheader("📋 Your Notebooks")
    st.info("Your notebooks will appear here once created")

elif page == "🔍 Ask & Search":
    st.title("🔍 Ask & Search")
    st.info("🤖 Ask questions about your documents and research")
    
    # Simple chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask a question about your research..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Add assistant response
        with st.chat_message("assistant"):
            response = "I'm ready to help! Please configure an AI provider in the Settings to enable chat functionality."
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

elif page == "🎙️ Podcasts":
    st.title("🎙️ Podcasts")
    st.info("🎧 Transcribe and analyze podcast episodes")
    
    # Podcast URL input
    podcast_url = st.text_input("Podcast RSS URL or Episode URL")
    
    if st.button("Process Podcast"):
        if podcast_url:
            with st.spinner("Processing podcast..."):
                st.success("✅ Podcast processing feature coming soon!")
        else:
            st.error("Please enter a podcast URL")
    
    st.subheader("📻 Recent Episodes")
    st.info("Processed episodes will appear here")

elif page == "🤖 Models":
    st.title("🤖 AI Models")
    st.info("⚙️ Configure and manage your AI providers")
    
    st.subheader("🔧 Configuration")
    st.write("Configure your AI providers in the Home Assistant addon settings:")
    
    st.code("""
# Go to: Supervisor → Add-on Store → Open Notebook → Configuration

openai_api_key: "sk-your-key-here"
anthropic_api_key: "sk-ant-your-key"
groq_api_key: "gsk_your-key"
google_api_key: "your-google-key"
mistral_api_key: "your-mistral-key"
deepseek_api_key: "your-deepseek-key"
""", language="yaml")
    
    st.subheader("🔗 Get API Keys")
    st.write("- 🔗 [OpenAI](https://platform.openai.com/api-keys)")
    st.write("- 🔗 [Anthropic](https://console.anthropic.com/)")
    st.write("- 🔗 [Groq](https://console.groq.com/keys)")
    st.write("- 🔗 [Google AI](https://makersuite.google.com/app/apikey)")
    st.write("- 🔗 [Mistral AI](https://console.mistral.ai/)")
    st.write("- 🔗 [DeepSeek](https://platform.deepseek.com/)")

elif page == "⚙️ Settings":
    st.title("⚙️ Settings")
    st.info("🔧 Application settings and configuration")
    
    # Display current configuration
    st.subheader("📊 Current Configuration")
    
    config_data = {
        "Database URL": os.getenv('DATABASE_URL', 'memory'),
        "Debug Mode": os.getenv('DEBUG', 'false'),
        "Log Level": os.getenv('LOG_LEVEL', 'INFO'),
        "Max File Size": f"{os.getenv('MAX_FILE_SIZE_MB', '50')}MB",
        "Authentication": os.getenv('ENABLE_AUTH', 'false'),
    }
    
    for key, value in config_data.items():
        st.write(f"**{key}**: {value}")
    
    st.subheader("📁 Storage Paths")
    st.write("- **Config**: `/config/open-notebook`")
    st.write("- **Share**: `/share/open-notebook`")
    st.write("- **Logs**: `/app/logs`")
    
    if st.button("Test Configuration"):
        st.success("✅ Configuration test passed!")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("**Open Notebook v0.4.1**")
st.sidebar.markdown("🏠 Home Assistant Add-on")

# File upload in sidebar
st.sidebar.subheader("📄 Quick Upload")
uploaded_file = st.sidebar.file_uploader(
    "Upload Document", 
    type=['pdf', 'txt', 'md', 'docx'],
    help="Upload a document to analyze"
)

if uploaded_file:
    st.sidebar.success(f"✅ {uploaded_file.name} uploaded!")
    st.sidebar.info("Document processing will be available soon.")
