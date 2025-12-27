import streamlit as st
import streamlit.components.v1 as components
import os

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(layout="wide", page_title="NAPASNEK QBANK")

# ---------------------------------------------------------
# 1. FILE LOADER & LINK PATCHER
# ---------------------------------------------------------
def load_and_patch_html(page_name):
    """
    1. Finds the correct file (ignoring capitalization).
    2. Reads the HTML.
    3. Replaces standard links (href="page.html") with Streamlit links (href="?page=name" target="_top").
    """
    
    # Mapping "URL names" to "File names"
    # The keys match the ?page= parameter
    file_map = {
        "home": "index.html",
        "biochemistry": "biochemistry.html",
        "physiology": "physiology.html",
        "anatomy": "Anatomy.html"  # Note the capital 'A' matching your file
    }
    
    target_filename = file_map.get(page_name, "index.html")
    
    # A. FIND THE FILE (Case-Insensitive Handling)
    real_path = None
    if os.path.exists(target_filename):
        real_path = target_filename
    else:
        # Fallback: look for the file ignoring case
        for f in os.listdir():
            if f.lower() == target_filename.lower():
                real_path = f
                break
    
    if not real_path:
        return None, f"File not found: {target_filename}"

    # B. READ CONTENT
    with open(real_path, "r", encoding='utf-8') as f:
        html_content = f.read()

    # C. PATCH LINKS (The Critical Fix)
    # We replace local file links with query parameters + target="_top".
    # target="_top" forces the whole browser tab to reload, which is required for Streamlit navigation.
    
    replacements = {
        'href="index.html"': 'href="?page=home" target="_top"',
        'href="biochemistry.html"': 'href="?page=biochemistry" target="_top"',
        'href="physiology.html"': 'href="?page=physiology" target="_top"',
        'href="anatomy.html"': 'href="?page=anatomy" target="_top"',
        'href="Anatomy.html"': 'href="?page=anatomy" target="_top"',
        
        # Handle single quotes just in case
        "href='index.html'": "href='?page=home' target='_top'",
        "href='biochemistry.html'": "href='?page=biochemistry' target='_top'",
        "href='physiology.html'": "href='?page=physiology' target='_top'",
        "href='anatomy.html'": "href='?page=anatomy' target='_top'",
        "href='Anatomy.html'": "href='?page=anatomy' target='_top'"
    }

    for old_link, new_link in replacements.items():
        html_content = html_content.replace(old_link, new_link)

    return html_content, None

# ---------------------------------------------------------
# 2. APP EXECUTION
# ---------------------------------------------------------

# Get current page from URL (defaults to 'home')
query_params = st.query_params
current_page = query_params.get("page", "home")

# Load the content
html_code, error_msg = load_and_patch_html(current_page)

if html_code:
    # Render the patched HTML
    # height=1000 ensures full visibility
    components.html(html_code, height=1000, scrolling=True)
else:
    # Error Screen
    st.error("⚠️ **System Error: File Not Found**")
    st.warning(error_msg)
    st.info(f"Attempted to load page: `{current_page}`")
    st.write("Files detected in folder:", os.listdir())
