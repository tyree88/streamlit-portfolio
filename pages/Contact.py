"""
Contact page for the Streamlit portfolio.
"""

import streamlit as st
from config import SITE_CONFIG
from components.contact_form import contact_form
from components.footer import create_footer


def main():
    """Main function to render the Contact page."""
    # Page configuration
    st.set_page_config(
        page_title=f"Contact | {SITE_CONFIG['title']}",
        page_icon=SITE_CONFIG["icon"],
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    # Header
    st.title("Contact Me")
    
    # Contact information
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("""
        ## Get In Touch
        
        I'm always open to discussing new projects, creative ideas, or opportunities to be part of your vision.
        
        Feel free to reach out to me through the contact form or via the following channels:
        """)
        
        # Contact details
        st.markdown(f"📧 **Email:** [{SITE_CONFIG['email']}](mailto:{SITE_CONFIG['email']})")
        
        if "linkedin" in SITE_CONFIG and SITE_CONFIG["linkedin"]:
            st.markdown(f"💼 **LinkedIn:** [Profile]({SITE_CONFIG['linkedin']})")
        
        if "github" in SITE_CONFIG and SITE_CONFIG["github"]:
            st.markdown(f"💻 **GitHub:** [Profile]({SITE_CONFIG['github']})")
        
        # Add more contact methods if needed
        st.markdown("""
        ## Response Time
        
        I typically respond to inquiries within 24-48 hours. For urgent matters, 
        please indicate so in your message.
        """)
    
    with col2:
        # Contact form
        contact_form(receiver_email=SITE_CONFIG.get("email"))
    
    # Footer
    create_footer()


if __name__ == "__main__":
    main() 