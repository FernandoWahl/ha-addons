import os
import streamlit as st


def check_password():
    """
    Check if the user has entered the correct password.
    Returns True if authenticated or no password is set.
    """
    # Get the password from environment variable (using our config)
    enable_auth = os.getenv('ENABLE_AUTH', 'false').lower() == 'true'
    app_password = os.getenv('AUTH_PASSWORD', '')
    
    # If authentication is disabled, skip
    if not enable_auth or not app_password:
        return True
    
    # Check if already authenticated in this session
    if "authenticated" in st.session_state and st.session_state.authenticated:
        return True
    
    # Show login form
    st.markdown("### 🔒 Open Notebook - Authentication Required")
    st.markdown("This Open Notebook instance is password protected.")
    
    with st.form("login_form"):
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            username = st.text_input("Username", value=os.getenv('AUTH_USERNAME', ''))
            password = st.text_input("Password", type="password", placeholder="Enter password")
            login_button = st.form_submit_button("🔑 Login", use_container_width=True)
    
    if login_button:
        auth_username = os.getenv('AUTH_USERNAME', '')
        auth_password = os.getenv('AUTH_PASSWORD', '')
        
        if username == auth_username and password == auth_password:
            st.session_state.authenticated = True
            st.success("✅ Authentication successful!")
            st.rerun()
        else:
            st.error("❌ Invalid credentials!")
    
    # Show help
    with st.expander("🔧 Configuration Help"):
        st.write("**Administrator:** Configure in addon settings:")
        st.code("""
enable_auth: true
auth_username: "your_username"  
auth_password: "your_password"
""", language="yaml")
    
    return False


def show_logout():
    """Show logout button in sidebar if authenticated"""
    enable_auth = os.getenv('ENABLE_AUTH', 'false').lower() == 'true'
    
    if enable_auth and st.session_state.get('authenticated', False):
        st.sidebar.markdown("---")
        if st.sidebar.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.rerun()
        
        username = os.getenv('AUTH_USERNAME', 'User')
        st.sidebar.write(f"👤 **{username}**")
