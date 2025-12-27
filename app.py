import streamlit as st
import streamlit.components.v1 as components
import os
import re

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(layout="wide", page_title="NAPASNEK QBANK")

# Credentials
VALID_USERNAME = "napasnek"
VALID_PASSWORD = "napasnek2028"

# ---------------------------------------------------------
# 1. SESSION STATE SETUP (Memory)
# ---------------------------------------------------------
# This remembers if you are logged in, even when pages change.
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# ---------------------------------------------------------
# 2. LOGIN SYSTEM (Python Native)
# ---------------------------------------------------------
def login_screen():
    st.markdown("""
        <style>
            .login-container {
                max-width: 400px;
                margin: 100px auto;
                padding: 2rem;
                background: white;
                border-radius: 10px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.1);
                text-align: center;
                font-family: 'Segoe UI', sans-serif;
            }
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        st.title("🔒 Login")
        user = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Access Portal", type="primary"):
            if user == VALID_USERNAME and password == VALID_PASSWORD:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid Credentials")

# ---------------------------------------------------------
# 3. HTML CLEANER
# ---------------------------------------------------------
def clean_html_for_streamlit(page_name):
    """
    Reads the HTML files and modifies them to work inside Streamlit.
    """
    files = {
        "home": "index.html",
        "biochemistry": "biochemistry.html",
        "physiology": "physiology.html",
        "anatomy": "Anatomy.html"
    }
    
    filename = files.get(page_name, "index.html")
    
    # Robust File Finder (Case Insensitive)
    if not os.path.exists(filename):
        for f in os.listdir():
            if f.lower() == filename.lower():
                filename = f
                break
    
    with open(filename, "r", encoding="utf-8") as f:
        html = f.read()

    # --- SPECIAL FIX FOR DASHBOARD (index.html) ---
    if page_name == "home":
        # 1. Remove the HTML Login Overlay (since Python handles it now)
        html = re.sub(r'<div id="login-overlay">.*?</div>', '', html, flags=re.DOTALL)
        
        # 2. Force the dashboard to be visible (it was hidden by default in your CSS)
        html = html.replace('display: none;', 'display: flex;') 
        html = html.replace('#dashboard-content {', '#dashboard-content { display: block !important;')

    # --- FIX ALL LINKS ---
    # Convert standard links to Streamlit URL parameters
    replacements = {
        'href="biochemistry.html"': 'href="?page=biochemistry" target="_self"',
        'href="physiology.html"':   'href="?page=physiology" target="_self"',
        'href="anatomy.html"':      'href="?page=anatomy" target="_self"',
        'href="Anatomy.html"':      'href="?page=anatomy" target="_self"',
        'href="index.html"':        'href="?page=home" target="_self"'
    }
    
    for old, new in replacements.items():
        html = html.replace(old, new)
        
    return html

# ---------------------------------------------------------
# 4. MAIN APP LOGIC
# ---------------------------------------------------------

if not st.session_state.logged_in:
    login_screen()
else:
    # Get current page from URL
    query_params = st.query_params
    page = query_params.get("page", "home")
    
    # Load the HTML content
    try:
        html_content = clean_html_for_streamlit(page)
        
        if page == "home":
            # For the Dashboard, we use st.markdown so links allow navigation
            # We wrap it in a div to ensure styling applies
            st.markdown(html_content, unsafe_allow_html=True)
            
            # Hide default Streamlit padding for a cleaner look
            st.markdown("""
                <style>
                    .block-container { padding-top: 1rem; padding-bottom: 0rem; }
                    header { visibility: hidden; }
                    footer { visibility: hidden; }
                </style>
            """, unsafe_allow_html=True)
            
        else:
            # For Quiz Pages (Anatomy/Physio/Bio), we MUST use components.html
            # because they contain complex JavaScript for the quiz logic.
            # We inject a <base> tag to ensure the "Back" button works.
            html_content = '<base target="_top">' + html_content
            components.html(html_content, height=1000, scrolling=True)
            
    except Exception as e:
        st.error("Error loading file. Please ensure index.html, Anatomy.html, biochemistry.html, and physiology.html are in this folder.")
        st.code(e)
