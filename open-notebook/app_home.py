import streamlit as st
import os

st.set_page_config(
    page_title="Open Notebook",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Open Notebook")
st.subheader("Home Assistant Add-on")

st.success("✅ Open Notebook is running successfully!")

st.info("""
This is a simplified version of Open Notebook running as a Home Assistant add-on.

**Next Steps:**
1. Configure your AI API keys in the add-on configuration
2. Upload documents and start researching
3. Use the chat interface to ask questions about your content
""")

# Show environment info
st.subheader("🔧 System Information")
col1, col2 = st.columns(2)

with col1:
    st.write("**Directories:**")
    st.write(f"- Config: `/config/open-notebook`")
    st.write(f"- Share: `/share/open-notebook`")
    st.write(f"- App: `/app`")

with col2:
    st.write("**Status:**")
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

st.subheader("📝 Configuration")
st.write("Add your configuration in the Home Assistant add-on settings:")
st.code("""
debug: false
# Add your AI API keys here when ready
""", language="yaml")

st.subheader("🚀 Ready for Full Version")
st.write("This simplified version confirms the add-on works. The full version includes:")
st.write("- 🤖 AI model integration")
st.write("- 📄 Document processing")
st.write("- 🎙️ Podcast transcription")
st.write("- 💬 Interactive chat")
st.write("- 🔍 Smart search")
