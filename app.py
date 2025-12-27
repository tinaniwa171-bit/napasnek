import streamlit as st
import streamlit.components.v1 as components
import os
import re

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(layout="wide", page_title="NAPASNEK QBANK")

# ---------------------------------------------------------
# 1. FILE FINDER (Handles Capitalization Errors)
# ---------------------------------------------------------
def get_file_content(target_filename):
    """
    Finds a file even if the capitalization is wrong
    (e.g., finds 'Anatomy.html' even if you ask for 'anatomy.html').
    """
    # 1. Try to find the file exactly as requested
    if os.path.exists(target_filename):
        with open(target_filename, "r", encoding='utf-8') as f:
            return f.read()
            
    # 2. If not found, look for it case-insensitive
    # (Fixes the issue where your file is Anatomy.html but link is anatomy.html)
    for f in os.listdir():
        if f.lower() == target_filename.lower():
            with open(f, "r", encoding='utf-8') as file:
                return file.read()
                
    return None

# ---------------------------------------------------------
# 2. THE FIX: REGEX LINK REPLACER
# ---------------------------------------------------------
def replace_links(html_content):
    """
    This function scans the HTML for any links (href="...") 
    and converts them into Streamlit navigation links.
    """
    
    # This function decides what to replace the link with
    def link_logic(match):
        original_link = match.group(1).lower() # Get the link text (e.g., anatomy.html)
        
        # Determine the target page based on the filename
        if "biochemistry" in original_link:
            return 'href="?page=biochemistry" target="_top"'
        elif "physiology" in original_link:
            return 'href="?page=physiology" target="_top"'
        elif "anatomy" in original_link:
            return 'href="?page=anatomy" target="_top"'
        elif "index" in original_link or "home" in original_link:
            return 'href="?page=home" target="_top"'
        else:
            # If it's a link we don't recognize, don't change it
            return match.group(0)

    # Use Regex to find ALL links ending in .html (handles " or ' quotes)
    # Pattern looks for: href="something.html"
    new_html = re.sub(
        r'href=["\']([^"\']+\.html)["\']', 
        link_logic, 
        html_content, 
        flags=re.IGNORECASE
    )
    
    return new_html

# ---------------------------------------------------------
# 3. MAIN APP LOGIC
# ---------------------------------------------------------

# A. Check URL to see which page we are on
# If no page is selected, default to 'home' (index.html)
query_params = st.query_params
current_page_name = query_params.get("page", "home")

# Map the page names to the likely file names
# (We map 'home' to 'index.html', others are just name + .html)
filename_map = {
    "home": "index.html",
    "biochemistry": "biochemistry.html",
    "physiology": "physiology.html",
    "anatomy": "Anatomy.html" # Note: Your file is capital A
}

target_file = filename_map.get(current_page_name, "index.html")

# B. Load the content
html_code = get_file_content(target_file)

if html_code:
    # C. Patch the links so they work in Streamlit
    fixed_html = replace_links(html_code)
    
    # D. Render the result
    components.html(fixed_html, height=1000, scrolling=True)

else:
    # Error Screen if files are missing
    st.error("⚠️ **System Error: File Not Found**")
    st.warning(f"The app tried to load `{target_file}` but couldn't find it.")
    st.info("Please verify that `index.html`, `Anatomy.html`, `biochemistry.html`, and `physiology.html` are all in the same folder.")
    st.write("Files currently in this folder:", os.listdir())
