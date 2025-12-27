import streamlit as st
import streamlit.components.v1 as components
import os

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(layout="wide", page_title="NAPASNEK QBANK")

# Map your "clean" URL names to the actual filenames
# Note: Ensure the filenames here match EXACTLY what is in your folder
FILES = {
    "home": "index.html",
    "biochemistry": "biochemistry.html",
    "physiology": "physiology.html",
    "anatomy": "Anatomy.html"  # User uploaded this as 'Anatomy.html' (Capital A)
}

# ---------------------------------------------------------
# APP LOGIC
# ---------------------------------------------------------

# 1. Determine which page to show based on the URL query parameter
# Example: ?page=anatomy loads Anatomy.html
query_params = st.query_params
current_page = query_params.get("page", "home")

# 2. Get the corresponding filename
if current_page not in FILES:
    current_page = "home"
    
file_name = FILES[current_page]

# 3. Check if file exists to prevent errors
if not os.path.exists(file_name):
    # Try case-insensitive fallback (e.g., if link is anatomy.html but file is Anatomy.html)
    found = False
    for f in os.listdir():
        if f.lower() == file_name.lower():
            file_name = f
            found = True
            break
    
    if not found:
        st.error(f"⚠️ Error: The file `{file_name}` was not found in the directory.")
        st.info("Please make sure `index.html`, `Anatomy.html`, `biochemistry.html`, and `physiology.html` are all in the same folder as `app.py`.")
        st.stop()

# 4. Read the HTML file content
with open(file_name, "r", encoding='utf-8') as f:
    html_content = f.read()

# ---------------------------------------------------------
# LINK PATCHING SYSTEM
# ---------------------------------------------------------
# This is the "Magic" part.
# Standard HTML links (href="anatomy.html") won't work inside a Streamlit component iframe.
# We replace them with query parameters (href="?page=anatomy") and target="_top".
# This forces the whole Streamlit app to reload and navigate to the correct page.

replacements = {
    # Replace Links to Biochemistry
    'href="biochemistry.html"': 'href="?page=biochemistry" target="_top"',
    "href='biochemistry.html'": "href='?page=biochemistry' target='_top'",
    
    # Replace Links to Physiology
    'href="physiology.html"': 'href="?page=physiology" target="_top"',
    "href='physiology.html'": "href='?page=physiology' target='_top'",
    
    # Replace Links to Anatomy (handling lowercase link from index vs uppercase filename)
    'href="anatomy.html"': 'href="?page=anatomy" target="_top"',
    "href='anatomy.html'": "href='?page=anatomy' target='_top'",
    'href="Anatomy.html"': 'href="?page=anatomy" target="_top"',
    
    # Replace Links back to Dashboard
    'href="index.html"': 'href="?page=home" target="_top"',
    "href='index.html'": "href='?page=home' target='_top'"
}

# Apply the replacements to the HTML string
for old_link, new_link in replacements.items():
    html_content = html_content.replace(old_link, new_link)

# ---------------------------------------------------------
# RENDER
# ---------------------------------------------------------
# Render the patched HTML. 
# height=1000 ensures it takes up most of the screen.
components.html(html_content, height=1000, scrolling=True)