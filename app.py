import streamlit as st
import streamlit.components.v1 as components
import os

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(layout="wide", page_title="NAPASNEK QBANK")

# ---------------------------------------------------------
# 1. SETUP FILE PATHS
# ---------------------------------------------------------
# This dictionary maps the "ID" of the page to the ACTUAL filename.
# We map both lowercase 'anatomy' and 'Anatomy' to be safe.
FILE_MAP = {
    "home": "index.html",
    "biochemistry": "biochemistry.html",
    "physiology": "physiology.html",
    "anatomy": "Anatomy.html", 
    "Anatomy": "Anatomy.html"
}

# ---------------------------------------------------------
# 2. HELPER FUNCTION: LOAD & FIX HTML
# ---------------------------------------------------------
def load_html(page_id):
    # 1. Get the filename from our map, default to index.html
    filename = FILE_MAP.get(page_id, "index.html")
    
    # 2. Check if file exists
    if not os.path.exists(filename):
        st.error(f"❌ File not found: {filename}")
        st.info("Make sure all HTML files are in the same folder as app.py")
        st.stop()
        
    # 3. Read the file
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
        
    # 4. THE FIX: MANUALLY REPLACE LINKS
    # We turn standard file links into Streamlit Navigation Commands.
    # target="_top" is CRITICAL. It forces the whole browser tab to reload.
    
    replacements = {
        # Fix Dashboard Links
        'href="biochemistry.html"': 'href="?page=biochemistry" target="_top"',
        'href="physiology.html"':   'href="?page=physiology" target="_top"',
        'href="anatomy.html"':      'href="?page=anatomy" target="_top"',
        'href="Anatomy.html"':      'href="?page=anatomy" target="_top"',
        
        # Fix "Back to Dashboard" Links
        'href="index.html"':        'href="?page=home" target="_top"',
        
        # Handle single quotes just in case (href='...')
        "href='biochemistry.html'": "href='?page=biochemistry' target='_top'",
        "href='physiology.html'":   "href='?page=physiology' target='_top'",
        "href='anatomy.html'":      "href='?page=anatomy' target='_top'",
        "href='Anatomy.html'":      "href='?page=anatomy' target='_top'",
        "href='index.html'":        "href='?page=home' target='_top'"
    }
    
    for old_link, new_link in replacements.items():
        content = content.replace(old_link, new_link)
        
    return content

# ---------------------------------------------------------
# 3. MAIN APP LOGIC
# ---------------------------------------------------------

# A. Check URL for "?page=..."
# If no page is specified, default to 'home'
query_params = st.query_params
current_page = query_params.get("page", "home")

# B. Load the patched HTML
html_content = load_html(current_page)

# C. Render the HTML
# height=1000 ensures it fills the screen. 
# scrolling=True allows you to scroll down if the quiz is long.
components.html(html_content, height=1000, scrolling=True)