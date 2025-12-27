import streamlit as st
import streamlit.components.v1 as components
import os
import re

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(layout="wide", page_title="NAPASNEK QBANK")

# 1. FILE MAPPING
# We use this to know which real file to open when a "page name" is requested.
# Keys are the "page" names used in the URL (?page=anatomy).
# Values are the ACTUAL filenames on your disk.
FILES = {
    "home": "index.html",
    "biochemistry": "biochemistry.html",
    "physiology": "physiology.html",
    "anatomy": "Anatomy.html"  # Note the capital 'A' to match your file
}

# ---------------------------------------------------------
# HELPER: FIND FILE CASE-INSENSITIVE
# ---------------------------------------------------------
def get_real_filename(target_filename):
    """Finds the file even if you messed up the capitalization."""
    if os.path.exists(target_filename):
        return target_filename
    
    # Search directory for a match ignoring case
    for f in os.listdir():
        if f.lower() == target_filename.lower():
            return f
    return None

# ---------------------------------------------------------
# APP LOGIC
# ---------------------------------------------------------

# 2. GET CURRENT PAGE FROM URL
# Defaults to "home" if ?page= is missing
query_params = st.query_params
current_page = query_params.get("page", "home")

# Fallback if the requested page is not in our dictionary
if current_page not in FILES:
    current_page = "home"

target_file = FILES[current_page]
real_file_path = get_real_filename(target_file)

# 3. ERROR HANDLING (If file is missing)
if not real_file_path:
    st.error(f"⚠️ **System Error:** Could not find the file `{target_file}`.")
    st.info(f"Current Directory: `{os.getcwd()}`")
    st.write("Files found here:", os.listdir())
    st.stop()

# 4. READ HTML CONTENT
with open(real_file_path, "r", encoding='utf-8') as f:
    html_content = f.read()

# ---------------------------------------------------------
# THE FIX: REGEX LINK PATCHING
# ---------------------------------------------------------
# This function intercepts ANY link ending in .html and converts it
# to a Streamlit-friendly navigation command.

def replace_link(match):
    # Extract the full link (e.g., "anatomy.html" or "Anatomy.html")
    original_link = match.group(1)
    lower_link = original_link.lower()

    # Map the HTML file to the ?page= parameter
    if "biochemistry" in lower_link:
        new_target = "?page=biochemistry"
    elif "physiology" in lower_link:
        new_target = "?page=physiology"
    elif "anatomy" in lower_link:
        new_target = "?page=anatomy"
    elif "index" in lower_link: # Back to dashboard
        new_target = "?page=home"
    else:
        # If it's some other link we don't know, leave it alone
        return match.group(0)
    
    # Return the new constructed link with target="_top" (forces reload)
    return f'href="{new_target}" target="_top"'

# Use Regex to find href="something.html" or href='something.html'
# This handles spaces, single quotes, double quotes, etc.
html_content = re.sub(
    r'href=["\']([^"\']+\.html)["\']', 
    replace_link, 
    html_content, 
    flags=re.IGNORECASE
)

# ---------------------------------------------------------
# RENDER
# ---------------------------------------------------------
components.html(html_content, height=1000, scrolling=True)
