"""
Contact page for the Streamlit portfolio.
"""

import streamlit as st
from config import SITE_CONFIG
from components.contact_form import contact_form
from components.footer import create_footer
from streamlit_shadcn_ui import card
from streamlit_shadcn_ui import button
from streamlit_shadcn_ui.py_components.badges import badges


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
        with card(key="contact_info_card", class_name="mb-4"):
            st.markdown("""
            ## Get In Touch
            
            I'm always open to discussing new projects, creative ideas, or opportunities to be part of your vision.
            
            Feel free to reach out to me through the contact form or via the following channels:
            """)
            
            # Contact details with badges
            st.markdown("### Contact Details")
            
            # Email badge
            badges([(f"📧 {SITE_CONFIG['email']}", "outline")], key="email_badge")
            
            # LinkedIn badge
            if "linkedin" in SITE_CONFIG and SITE_CONFIG["linkedin"]:
                badges([("💼 LinkedIn", "outline")], key="linkedin_badge")
                
            # GitHub badge
            if "github" in SITE_CONFIG and SITE_CONFIG["github"]:
                badges([("💻 GitHub", "outline")], key="github_badge")
            
            # Response time info
            st.markdown("""
            ## Response Time
            
            I typically respond to inquiries within 24-48 hours. For urgent matters, 
            please indicate so in your message.
            """)
            
            # Social links as buttons
            st.markdown("### Connect")
            
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                if "github" in SITE_CONFIG and SITE_CONFIG["github"]:
                    button("GitHub Profile", variant="default", size="sm", key="github_contact_btn", class_name="w-full")
            
            with col_btn2:
                if "linkedin" in SITE_CONFIG and SITE_CONFIG["linkedin"]:
                    button("LinkedIn Profile", variant="outline", size="sm", key="linkedin_contact_btn", class_name="w-full")
    
    with col2:
        # Contact form wrapped in a card
        with card(key="contact_form_card", class_name="mb-4"):
            # Contact form
            contact_form(receiver_email=SITE_CONFIG.get("email"))
    
    # Footer
    create_footer()


if __name__ == "__main__":
    main() 