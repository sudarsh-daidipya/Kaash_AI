import streamlit as st
from basic_tier import basic_ui
from premium_tier import premium_ui

# Page Configuration
st.set_page_config(page_title="Kaash Analytics Engine", page_icon="📊", layout="wide")

def login_page():
    st.title("🔐 Login to Kaash Analytics")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")
        
        if submit_button:
            if username == "admin" and password == "1234":
                st.session_state['logged_in'] = True
                # Set default landing tier after login
                st.session_state['current_module'] = "Premium: Data Matchmaker" 
                st.rerun()
            else:
                st.error("Invalid username or password.")

def main():
    # Initialize session state for login
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    # Route to login page if not logged in
    if not st.session_state['logged_in']:
        login_page()
    else:
        # Sidebar Navigation
        st.sidebar.title("📊 Kaash Analytics")
        st.sidebar.markdown("---")
        
        # Dynamic module selector (Radio Buttons)
        selected_module = st.sidebar.radio(
            "Select Module:",
            ("Basic: Automated EDA", "Premium: Data Matchmaker"),
            index=1 # Defaults to Premium since we are working on it
        )
        
        st.sidebar.markdown("---")
        
        # Logout Button
        if st.sidebar.button("Logout"):
            st.session_state['logged_in'] = False
            st.rerun()
            
        # Main Page Routing based on sidebar selection
        if "Basic" in selected_module:
            basic_ui.render_page()
        elif "Premium" in selected_module:
            premium_ui.render_page()

if __name__ == "__main__":
    main()