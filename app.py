import streamlit as st
import streamlit.components.v1 as components
import os

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(layout="wide", page_title="NAPASNEK QBANK")

# ---------------------------------------------------------
# 1. FILE FINDER (Handles Capitalization Issues)
# ---------------------------------------------------------
def get_file_content(page_name):
    # Mapping of "URL names" to "File names"
    # We map strictly to the files you uploaded
    mapping = {
        "home": "index.html",
        "biochemistry": "biochemistry.html",
        "physiology": "physiology.html",
        "anatomy": "Anatomy.html" # Capital A as per your upload
    }
    
    target_filename = mapping.get(page_name, "index.html")
    
    # Logic: Try to find the file. If exact name fails, try lowercase match.
    if os.path.exists(target_filename):
        with open(target_filename, "r", encoding='utf-8') as f:
            return f.read()
            
    # Fallback search
    for f in os.listdir():
        if f.lower() == target_filename.lower():
            with open(f, "r", encoding='utf-8') as file:
                return file.read()
                
    return None

# ---------------------------------------------------------
# 2. THE JAVASCRIPT FORCE FIX
# ---------------------------------------------------------
# This script is appended to every page. It grabs every <a> tag
# and forces it to behave like a Streamlit navigator.
force_nav_script = """
<script>
    document.addEventListener("DOMContentLoaded", function() {
        // Get all links on the page
        const links = document.querySelectorAll("a");
        
        links.forEach(link => {
            link.addEventListener('click', function(event) {
                // 1. Stop the link from trying to open a file (which fails)
                event.preventDefault(); 
                
                const href = this.getAttribute("href");
                
                if (href) {
                    let targetPage = 'home';
                    const lowerHref = href.toLowerCase();
                    
                    // 2. Decide where to go based on the link text
                    if (lowerHref.includes("anatomy")) {
                        targetPage = 'anatomy';
                    } else if (lowerHref.includes("biochemistry")) {
                        targetPage = 'biochemistry';
                    } else if (lowerHref.includes("physiology")) {
                        targetPage = 'physiology';
                    } else if (lowerHref.includes("index") || lowerHref.includes("home")) {
                        targetPage = 'home';
                    }
                    
                    // 3. Force the PARENT window (Streamlit) to reload with the new page
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

# A. Read URL to decide what to show
query_params = st.query_params
current_page = query_params.get("page", "home")

# B. Load the raw HTML from the file
html_content = get_file_content(current_page)

if html_content:
    # C. Inject the Javascript Fix at the end of the file
    final_html = html_content + force_nav_script
    
    # D. Render
    components.html(final_html, height=1000, scrolling=True)

else:
    st.error("⚠️ **System Error: File Not Found**")
    st.info(f"The app tried to load the page: `{current_page}`")
    st.write("Files found in folder:", os.listdir())
