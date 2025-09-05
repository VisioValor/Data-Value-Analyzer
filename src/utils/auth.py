"""
Authentication utilities for VisioValor Data Valuation App
"""
import streamlit as st
from datetime import datetime, timedelta

# Simple user database (in production, use a proper database)
USERS_DB = {
    "admin": {
        "password": "D@ta4L1fe!",
        "role": "admin",
        "created_at": "2024-01-01"
    }
}

def authenticate_user(username, password):
    """Authenticate a user with username and password"""
    if username in USERS_DB:
        user_data = USERS_DB[username]
        if password == user_data["password"]:
            return {
                "username": username,
                "role": user_data["role"],
                "authenticated": True
            }
    return {"authenticated": False}

def create_session(user_info):
    """Create a user session"""
    st.session_state.authenticated = True
    st.session_state.user = user_info
    st.session_state.login_time = datetime.now()

def clear_session():
    """Clear user session"""
    if 'authenticated' in st.session_state:
        del st.session_state.authenticated
    if 'user' in st.session_state:
        del st.session_state.user
    if 'login_time' in st.session_state:
        del st.session_state.login_time

def is_authenticated():
    """Check if user is authenticated"""
    return st.session_state.get('authenticated', False)

def get_current_user():
    """Get current user information"""
    if is_authenticated():
        return st.session_state.get('user', {})
    return {}

def check_session_timeout():
    """Check if session has timed out (24 hours)"""
    if is_authenticated():
        login_time = st.session_state.get('login_time')
        if login_time:
            if datetime.now() - login_time > timedelta(hours=24):
                clear_session()
                return False
    return True

def display_login_form():
    """Display the login form"""
    st.markdown("""
    <div style="text-align: center; margin-bottom: 40px;">
        <h1 style="color: #262730; font-family: 'Source Sans Pro', Arial, sans-serif; font-size: 32px; font-weight: 600; margin: 0;">
            VisioValor
        </h1>
        <p style="color: #666; font-size: 16px; margin-top: 10px;">Data Valuation App</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        st.markdown("### 🔐 Sign In")
        
        username = st.text_input(
            "Username",
            placeholder="Enter your username",
            help="Enter your username to access the application"
        )
        
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            help="Enter your password to access the application"
        )
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submitted = st.form_submit_button(
                "Sign In",
                type="primary",
                use_container_width=True
            )
        
        if submitted:
            if username and password:
                user_info = authenticate_user(username, password)
                if user_info["authenticated"]:
                    create_session(user_info)
                    st.success(f"Welcome back, {user_info['username']}! 🎉")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password. Please try again.")
            else:
                st.warning("⚠️ Please enter both username and password.")

def display_logout_button():
    """Display logout button in sidebar"""
    if is_authenticated():
        user = get_current_user()
        st.sidebar.markdown("---")
        st.sidebar.markdown(f"**Logged in as:** {user.get('username', 'Unknown')}")
        
        if st.sidebar.button("🚪 Logout", type="secondary"):
            clear_session()
            st.rerun()
