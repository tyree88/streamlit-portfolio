"""
Contact page for the Streamlit portfolio.
"""

import streamlit as st
from config import SITE_CONFIG
from components.contact_form import contact_info
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
        with card(key="contact_info_card"):
            st.markdown("""
            ## Get In Touch
            
            I'm always open to discussing new projects, creative ideas, or opportunities to be part of your vision.
            
            Feel free to reach out to me through any of the social platforms listed below:
            """)
            
            # Contact details with badges
            st.markdown("### Connect On")
            
            # Social badges
            badge_list = []
            
            # LinkedIn badge
            if "linkedin" in SITE_CONFIG and SITE_CONFIG["linkedin"]:
                badge_list.append(("💼 LinkedIn", "outline"))
                
            # GitHub badge
            if "github" in SITE_CONFIG and SITE_CONFIG["github"]:
                badge_list.append(("💻 GitHub", "outline"))
                
            # Bluesky badge
            if "bluesky" in SITE_CONFIG and SITE_CONFIG["bluesky"]:
                badge_list.append(("🦋 Bluesky", "outline"))
            
            if badge_list:
                badges(badge_list, key="social_badges")
            
            # Social links as buttons
            st.markdown("### Connect")
            
            col_btn1, col_btn2, col_btn3 = st.columns(3)
            
            with col_btn1:
                if "github" in SITE_CONFIG and SITE_CONFIG["github"]:
                    button("GitHub Profile", variant="default", size="sm", key="github_contact_btn", class_name="w-full")
            
            with col_btn2:
                if "linkedin" in SITE_CONFIG and SITE_CONFIG["linkedin"]:
                    button("LinkedIn Profile", variant="outline", size="sm", key="linkedin_contact_btn", class_name="w-full")
            
            with col_btn3:
                if "bluesky" in SITE_CONFIG and SITE_CONFIG["bluesky"]:
                    button("Bluesky Profile", variant="secondary", size="sm", key="bluesky_contact_btn", class_name="w-full")
    
    with col2:
        # Contact info component wrapped in a card
        with card(key="contact_social_card"):
            contact_info(
                github_url=SITE_CONFIG.get("github"),
                linkedin_url=SITE_CONFIG.get("linkedin"),
                bluesky_url=SITE_CONFIG.get("bluesky"),
                key="contact_page"
            )
    
    # Footer
    create_footer()


if __name__ == "__main__":
    main() 