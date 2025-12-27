import streamlit as st
import streamlit.components.v1 as components
import os
import re

# ---------------------------------------------------------
# 1. APP CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="NAPASNEK QBANK",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit's default elements (Header, Footer, Menu) for a "Pro" look
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .block-container {
            padding-top: 0rem;
            padding-bottom: 0rem;
            padding-left: 0rem;
            padding-right: 0rem;
        }
        iframe {
            width: 100%;
            border: none;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. SESSION & LOGIN LOGIC
# ---------------------------------------------------------
# Credentials
VALID_USERNAME = "napasnek"
VALID_PASSWORD = "napasnek2028"

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def login_screen():
    # Use columns to center the login box
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.write("")
        st.write("") # Spacing
        st.write("")
        st.markdown("<h1 style='text-align: center; color: #2c3e50;'>🔒 NAPASNEK 2028</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #7f8c8d;'>Secure Student Portal</p>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            user = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Access Dashboard", type="primary", use_container_width=True)
            
            if submit:
                if user == VALID_USERNAME and password == VALID_PASSWORD:
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Invalid Credentials")

# ---------------------------------------------------------
# 3. HTML PROCESSING ENGINE
# ---------------------------------------------------------
def get_processed_html(page_name):
    """
    Reads the HTML file and modifies links to work with Streamlit navigation.
    """
    # Map 'page_name' from URL to actual 'filename'
    file_map = {
        "home": "index.html",
        "biochemistry": "biochemistry.html",
        "physiology": "physiology.html",
        "anatomy": "Anatomy.html" # Capital A matches your uploaded file
    }
    
    filename = file_map.get(page_name, "index.html")

    # 1. Robust File Loading (Case Insensitive Fallback)
    if not os.path.exists(filename):
        for f in os.listdir():
            if f.lower() == filename.lower():
                filename = f
                break
                
    if not os.path.exists(filename):
        return f"<h1 style='text-align:center; margin-top:50px;'>Error: File '{filename}' not found.</h1>"

    # 2. Read the file
    with open(filename, "r", encoding="utf-8") as f:
        html_content = f.read()

    # 3. FIX FOR INDEX.HTML (Disable JS Login / Show Dashboard)
    # Since we are using Python login, we strip the JS login UI from the HTML
    if page_name == "home":
        # Force the dashboard div to be visible
        html_content = html_content.replace('display: none;', 'display: flex;')
        # Hide the login overlay div using inline CSS injection
        html_content = html_content.replace('</head>', '<style>#login-overlay { display: none !important; } #dashboard-content { display: flex !important; }</style></head>')

    # 4. FIX NAVIGATION LINKS (The "Magic" Link Replacer)
    # We find href="page.html" and change it to href="?page=page_id" target="_top"
    # target="_top" forces the browser to reload the URL, triggering Streamlit to switch pages.
    
    replacements = {
        # Biochemistry
        'href="biochemistry.html"': 'href="?page=biochemistry" target="_top"',
        "href='biochemistry.html'": "href='?page=biochemistry' target='_top'",
        
        # Physiology
        'href="physiology.html"': 'href="?page=physiology" target="_top"',
        "href='physiology.html'": "href='?page=physiology' target='_top'",
        
        # Anatomy (Handles multiple capitalizations just in case)
        'href="anatomy.html"': 'href="?page=anatomy" target="_top"',
        "href='anatomy.html'": "href='?page=anatomy' target='_top'",
        'href="Anatomy.html"': 'href="?page=anatomy" target="_top"',
        "href='Anatomy.html'": "href='?page=anatomy' target='_top'",

        # Back to Home
        'href="index.html"': 'href="?page=home" target="_top"',
        "href='index.html'": "href='?page=home' target='_top'"
    }

    for old_link, new_link in replacements.items():
        html_content = html_content.replace(old_link, new_link)

    return html_content

# ---------------------------------------------------------
# 4. MAIN APP EXECUTION
# ---------------------------------------------------------
if not st.session_state.logged_in:
    login_screen()
else:
    # 1. Get the requested page from URL (defaults to 'home')
    query_params = st.query_params
    current_page = query_params.get("page", "home")

    # 2. Process the HTML to make it Streamlit-compatible
    final_html = get_processed_html(current_page)

    # 3. Render the HTML
    # We use a very high height to ensure no double scrollbars appear inside the component
    components.html(final_html, height=1200, scrolling=True)
