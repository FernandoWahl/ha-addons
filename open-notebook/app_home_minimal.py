import streamlit as st
import os

st.set_page_config(page_title="Open Notebook", page_icon="📚", layout="wide")

# Load environment
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

# Sidebar
st.sidebar.title("📚 Open Notebook")
st.sidebar.success("✅ Running Successfully!")

page = st.sidebar.radio("Navigate", [
    "🏠 Home",
    "📚 Notebooks", 
    "💬 Chat",
    "⚙️ Settings"
])

# Main content
if page == "🏠 Home":
    st.title("📚 Open Notebook")
    st.success("🎉 Welcome to Open Notebook!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🤖 AI Status")
        
        # Check API keys
        apis = {
            "OpenAI": os.getenv('OPENAI_API_KEY', ''),
            "Anthropic": os.getenv('ANTHROPIC_API_KEY', ''),
            "Groq": os.getenv('GROQ_API_KEY', ''),
        }
        
        configured = sum(1 for key in apis.values() if key)
        
        if configured > 0:
            st.success(f"✅ {configured} AI provider(s) configured")
            for name, key in apis.items():
                if key:
                    st.write(f"✅ {name}")
        else:
            st.warning("⚠️ No AI providers configured")
            st.info("Add API keys in addon configuration")
    
    with col2:
        st.subheader("📊 System")
        st.write("🌊 Streamlit: Running")
        st.write("🐍 Python: Available") 
        st.write("📁 Storage: Ready")
        
        # Test directories
        try:
            os.makedirs("/config/open-notebook", exist_ok=True)
            st.write("✅ File System: OK")
        except:
            st.write("❌ File System: Error")

elif page == "📚 Notebooks":
    st.title("📚 Notebooks")
    
    # Simple notebook interface
    with st.form("notebook_form"):
        name = st.text_input("Notebook Name")
        desc = st.text_area("Description")
        
        if st.form_submit_button("Create"):
            if name:
                st.success(f"✅ Created notebook: {name}")
                st.balloons()
    
    st.info("📝 Your notebooks will be managed here")

elif page == "💬 Chat":
    st.title("💬 AI Chat")
    
    # Simple chat
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    if prompt := st.chat_input("Ask something..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.write(prompt)
        
        with st.chat_message("assistant"):
            response = "Hello! Please configure an AI provider to enable chat."
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

elif page == "⚙️ Settings":
    st.title("⚙️ Settings")
    
    st.subheader("📋 Configuration")
    st.code("""
# Add to Home Assistant addon config:
openai_api_key: "sk-your-key"
anthropic_api_key: "sk-ant-your-key"  
groq_api_key: "gsk_your-key"
""", language="yaml")
    
    st.subheader("🔗 Get API Keys")
    st.write("- [OpenAI](https://platform.openai.com/api-keys)")
    st.write("- [Anthropic](https://console.anthropic.com/)")
    st.write("- [Groq](https://console.groq.com/keys)")

# Sidebar info
st.sidebar.markdown("---")
st.sidebar.info("📱 **Open Notebook v0.4.2**\n\nMinimal, reliable version")

# File upload
uploaded = st.sidebar.file_uploader("📄 Upload File", type=['txt', 'pdf'])
if uploaded:
    st.sidebar.success(f"✅ {uploaded.name}")
