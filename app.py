import streamlit as st
import streamlit.components.v1 as components
import os
import re

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(layout="wide", page_title="NAPASNEK QBANK")

# Credentials for the Python-side Login
VALID_USERNAME = "student"
VALID_PASSWORD = "admin123"

# ---------------------------------------------------------
# 1. SESSION STATE (Memory)
# ---------------------------------------------------------
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# ---------------------------------------------------------
# 2. LOGIN SCREEN (Python Native)
# ---------------------------------------------------------
def show_login():
    st.markdown("""
        <style>
            .stApp { background-color: #f4f7f6; }
            .login-box {
                max-width: 400px;
                margin: 50px auto;
                padding: 40px;
                background: white;
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                text-align: center;
            }
        </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.title("🔒 Login")
        user = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Enter Dashboard", type="primary", use_container_width=True):
            if user == VALID_USERNAME and password == VALID_PASSWORD:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Incorrect Username or Password")

# ---------------------------------------------------------
# 3. HTML PROCESSOR (The Magic Fix)
# ---------------------------------------------------------
def get_processed_html(page_name):
    # Map URL names to File names
    files = {
        "home": "index.html",
        "biochemistry": "biochemistry.html",
        "physiology": "physiology.html",
        "anatomy": "Anatomy.html" # Note Capital A
    }
    
    filename = files.get(page_name, "index.html")

    # A. Robust File Finding (Case Insensitive)
    if not os.path.exists(filename):
        for f in os.listdir():
            if f.lower() == filename.lower():
                filename = f
                break
    
    if not os.path.exists(filename):
        return f"<h1>Error: File {filename} not found.</h1>"

    # B. Read the File
    with open(filename, "r", encoding="utf-8") as f:
        html = f.read()

    # C. PATCH 1: REMOVE OLD LOGIN FROM INDEX.HTML
    # Your index.html has a JS login overlay. We must remove it so it doesn't block the view.
    if page_name == "home":
        # Remove the login overlay div
        html = re.sub(r'<div id="login-overlay">.*?</div>', '', html, flags=re.DOTALL)
        # Force dashboard to be visible (it was hidden by default in your CSS)
        html = html.replace('display: none;', 'display: flex;')
        html = html.replace('#dashboard-content {', '#dashboard-content { display: block !important;')

    # D. PATCH 2: REWRITE LINKS
    # We change href="anatomy.html" to href="?page=anatomy" target="_top"
    # target="_top" is CRITICAL. It forces the browser to reload the whole tab.
    
    replacements = {
        'href="biochemistry.html"': 'href="?page=biochemistry" target="_top"',
        'href="physiology.html"':   'href="?page=physiology" target="_top"',
        'href="anatomy.html"':      'href="?page=anatomy" target="_top"',
        'href="Anatomy.html"':      'href="?page=anatomy" target="_top"',
        'href="index.html"':        'href="?page=home" target="_top"',
        
        # Single quote variations
        "href='biochemistry.html'": "href='?page=biochemistry' target='_top'",
        "href='physiology.html'":   "href='?page=physiology' target='_top'",
        "href='anatomy.html'":      "href='?page=anatomy' target='_top'",
        "href='Anatomy.html'":      "href='?page=anatomy' target='_top'",
        "href='index.html'":        "href='?page=home' target='_top'"
    }
    
    for old, new in replacements.items():
        html = html.replace(old, new)
        
    return html

# ---------------------------------------------------------
# 4. MAIN APP LOGIC
# ---------------------------------------------------------

# Step 1: Check Login
if not st.session_state.logged_in:
    show_login()
else:
    # Step 2: Get Current Page from URL
    # When you click a link, the page reloads with ?page=anatomy
    query_params = st.query_params
    current_page = query_params.get("page", "home")
    
    # Step 3: Load and Fix the HTML
    html_content = get_processed_html(current_page)
    
    # Step 4: Display it
    # We use a large height to fit the whole quiz
    components.html(html_content, height=1200, scrolling=True)
    
    # Step 5: Clean up Streamlit UI (Hide header/footer)
    st.markdown("""
        <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            .block-container {padding-top: 0rem; padding-bottom: 0rem; padding-left:0; padding-right:0;}
        </style>
    """, unsafe_allow_html=True)
