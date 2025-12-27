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
# Maps the 'page' parameter in the URL to the ACTUAL filename.
# We handle both lowercase 'anatomy' and Capital 'Anatomy' here.
PAGE_MAP = {
    "home": "index.html",
    "biochemistry": "biochemistry.html",
    "physiology": "physiology.html",
    "anatomy": "Anatomy.html", # Capital A, matching your file
}

# ---------------------------------------------------------
# 2. HELPER: LOAD & FIX HTML LINKS
# ---------------------------------------------------------
def load_and_fix_html(page_name):
    # A. Determine which file to open
    filename = PAGE_MAP.get(page_name, "index.html")
    
    # B. Safety Check: Does the file exist?
    if not os.path.exists(filename):
        # Try case-insensitive fallback (e.g. finding Anatomy.html if anatomy.html requested)
        found = False
        for f in os.listdir():
            if f.lower() == filename.lower():
                filename = f
                found = True
                break
        if not found:
            return None, f"File not found: {filename}"

    # C. Read the file
    with open(filename, "r", encoding="utf-8") as f:
        html_content = f.read()

    # D. THE FIX: REPLACE LINKS
    # We essentially 'rewrite' your HTML before showing it.
    # We change standard file links to Streamlit Navigation links.
    # target="_top" forces the MAIN window to reload, not just the iframe.
    
    replacements = {
        # Dashboard Links -> Streamlit Navigation
        'href="biochemistry.html"': 'href="?page=biochemistry" target="_top"',
        'href="physiology.html"':   'href="?page=physiology" target="_top"',
        'href="anatomy.html"':      'href="?page=anatomy" target="_top"',
        'href="Anatomy.html"':      'href="?page=anatomy" target="_top"',
        'href="index.html"':        'href="?page=home" target="_top"',
        
        # Handle Single Quotes (just in case)
        "href='biochemistry.html'": "href='?page=biochemistry' target='_top'",
        "href='physiology.html'":   "href='?page=physiology' target='_top'",
        "href='anatomy.html'":      "href='?page=anatomy' target='_top'",
        "href='Anatomy.html'":      "href='?page=anatomy' target='_top'",
        "href='index.html'":        "href='?page=home' target='_top'"
    }
    
    for old, new in replacements.items():
        html_content = html_content.replace(old, new)
        
    return html_content, None

# ---------------------------------------------------------
# 3. MAIN APP LOGIC
# ---------------------------------------------------------

# A. Get current page from URL query params
query_params = st.query_params
current_page = query_params.get("page", "home")

# B. Load the content
html_data, error = load_and_fix_html(current_page)

if html_data:
    # C. Render the HTML
    # height=1000 ensures it fits on screen
    # scrolling=True allows you to scroll long quizzes
    components.html(html_data, height=1000, scrolling=True)
else:
    # Error Screen
    st.error("⚠️ System Error")
    st.warning(f"Could not load page: {error}")
    st.info("Please verify your file names match exactly: `index.html`, `Anatomy.html`, `biochemistry.html`, `physiology.html`")
    st.write("Files in current folder:", os.listdir())
