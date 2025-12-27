import streamlit as st
import streamlit.components.v1 as components
import os

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(layout="wide", page_title="NAPASNEK QBANK")

# ---------------------------------------------------------
# FILE SYSTEM LOGIC
# ---------------------------------------------------------
def get_file_content(page_name):
    """
    Smart file finder. It looks for the file even if you 
    accidentally capitalized it differently (e.g. 'anatomy.html' vs 'Anatomy.html').
    """
    # Map the URL ?page=name to the likely filename
    mapping = {
        "home": "index.html",
        "biochemistry": "biochemistry.html",
        "physiology": "physiology.html",
        "anatomy": "Anatomy.html" # Tries this first
    }
    
    target_filename = mapping.get(page_name, "index.html")
    
    # 1. Try exact match
    if os.path.exists(target_filename):
        with open(target_filename, "r", encoding='utf-8') as f:
            return f.read()
            
    # 2. Try case-insensitive search (Fixes 'anatomy.html' vs 'Anatomy.html' issues)
    for f in os.listdir():
        if f.lower() == target_filename.lower():
            with open(f, "r", encoding='utf-8') as file:
                return file.read()
                
    # 3. Error if not found
    return None

# ---------------------------------------------------------
# JAVASCRIPT NAVIGATION FIX (The Magic Part)
# ---------------------------------------------------------
# Instead of Python replacing text, we inject this Script into the HTML.
# It waits for the page to load, finds your links, and fixes them automatically.
nav_script = """
<script>
    document.addEventListener("DOMContentLoaded", function() {
        const links = document.querySelectorAll("a");
        links.forEach(link => {
            const href = link.getAttribute("href");
            if (href) {
                const lowerHref = href.toLowerCase();
                
                // If link goes to anatomy, force Streamlit navigation
                if (lowerHref.includes("anatomy.html")) {
                    link.href = "?page=anatomy";
                    link.target = "_top"; // Forces the whole page to reload
                } 
                else if (lowerHref.includes("biochemistry.html")) {
                    link.href = "?page=biochemistry";
                    link.target = "_top";
                }
                else if (lowerHref.includes("physiology.html")) {
                    link.href = "?page=physiology";
                    link.target = "_top";
                }
                else if (lowerHref.includes("index.html")) {
                    link.href = "?page=home";
                    link.target = "_top";
                }
            }
        });
    });
</script>
"""

# ---------------------------------------------------------
# APP EXECUTION
# ---------------------------------------------------------

# 1. Get current page from URL (defaults to 'home')
query_params = st.query_params
page = query_params.get("page", "home")

# 2. Load the HTML content
html_content = get_file_content(page)

if html_content:
    # 3. Inject the Navigation Script at the end of the <body>
    # This ensures your links work perfectly every time.
    final_html = html_content + nav_script
    
    # 4. Render
    components.html(final_html, height=1000, scrolling=True)
else:
    st.error("⚠️ **System Error:** Could not find the HTML files.")
    st.info(f"Looking for page: `{page}`")
    st.write("Files found in current folder:", os.listdir())
    st.warning("Please make sure `index.html`, `Anatomy.html`, `biochemistry.html`, and `physiology.html` are in the same folder as `app.py`.")
