import streamlit as st
import streamlit.components.v1 as components
import os

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(layout="wide", page_title="NAPASNEK QBANK")

# ---------------------------------------------------------
# 1. SMART FILE FINDER
# ---------------------------------------------------------
def get_file_content(page_name):
    """
    Finds the correct HTML file even if capitalization is different
    (e.g., finds 'Anatomy.html' when looking for 'anatomy.html').
    """
    # Map the URL ?page=name to the likely filename
    mapping = {
        "home": "index.html",
        "biochemistry": "biochemistry.html",
        "physiology": "physiology.html",
        "anatomy": "Anatomy.html"  # Your file has a capital 'A'
    }
    
    target_filename = mapping.get(page_name, "index.html")
    
    # Check current directory files to find a match (case-insensitive)
    if os.path.exists(target_filename):
        with open(target_filename, "r", encoding='utf-8') as f:
            return f.read()
            
    # Fallback: Scan directory if exact name not found
    for f in os.listdir():
        if f.lower() == target_filename.lower():
            with open(f, "r", encoding='utf-8') as file:
                return file.read()
                
    return None

# ---------------------------------------------------------
# 2. NAVIGATION SCRIPT (The Fix)
# ---------------------------------------------------------
# This Javascript forces the browser top window to reload when a link is clicked.
nav_script = """
<script>
    document.addEventListener("DOMContentLoaded", function() {
        const links = document.querySelectorAll("a");
        links.forEach(link => {
            link.addEventListener('click', function(event) {
                const href = this.getAttribute("href");
                if (href && href !== '#') {
                    event.preventDefault(); // Stop default behavior
                    
                    // Determine which page to load based on the link text
                    let targetPage = 'home';
                    const lowerHref = href.toLowerCase();
                    
                    if (lowerHref.includes("anatomy")) {
                        targetPage = 'anatomy';
                    } else if (lowerHref.includes("biochemistry")) {
                        targetPage = 'biochemistry';
                    } else if (lowerHref.includes("physiology")) {
                        targetPage = 'physiology';
                    } else if (lowerHref.includes("index")) {
                        targetPage = 'home';
                    }
                    
                    // Force the main browser window to navigate
                    window.top.location.href = "?page=" + targetPage;
                }
            });
        });
    });
</script>
"""

# ---------------------------------------------------------
# 3. APP EXECUTION
# ---------------------------------------------------------

# Get the current page from the URL query parameter (defaults to 'home')
query_params = st.query_params
page = query_params.get("page", "home")

# Load the HTML
html_content = get_file_content(page)

if html_content:
    # Inject the Navigation Script before the closing body tag
    # This ensures the script runs and attaches to your buttons
    if "</body>" in html_content:
        final_html = html_content.replace("</body>", nav_script + "</body>")
    else:
        final_html = html_content + nav_script
    
    # Render the HTML
    components.html(final_html, height=1000, scrolling=True)

else:
    st.error("⚠️ **System Error:** Could not find the HTML files.")
    st.warning(f"Attempted to load: {page}")
    st.info("Please make sure `index.html`, `Anatomy.html`, `biochemistry.html`, and `physiology.html` are in the same folder as `app.py`.")
    st.write("Files detected in current folder:", os.listdir())
