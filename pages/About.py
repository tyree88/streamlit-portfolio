"""
About page for the Streamlit portfolio.
"""

import streamlit as st
from config import SITE_CONFIG, CONTENT_CONFIG
from utils.display_utils import create_timeline, display_skills, load_css_file
from utils.data_utils import prepare_skills_data
from components.footer import create_footer
from components.contact_form import create_social_links
from components.navbar import create_navbar, initialize_navigation
from streamlit_shadcn_ui import card
from streamlit_shadcn_ui import button
from streamlit_shadcn_ui.py_components.badges import badges
from streamlit_shadcn_ui import avatar
import os


def load_css():
    """Load CSS files for the About page."""
    # Load common CSS
    load_css_file("assets/css/pages/common.css")
    # Load page-specific CSS
    load_css_file("assets/css/pages/about.css")


def main():
    """Main function to render the About page."""
    # Page configuration
    st.set_page_config(
        page_title=f"About | {SITE_CONFIG['title']}",
        page_icon=SITE_CONFIG["icon"],
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize navigation settings
    initialize_navigation()
    
    # Load custom CSS
    load_css()
    
    # Check if we have a section to scroll to from the navbar
    about_section = st.session_state.get("about_section", None)
    
    # Header
    st.markdown("<h1 class='main-header'>About Me</h1>", unsafe_allow_html=True)
    
    # Add section anchor for profile
    st.markdown("<div id='profile'></div>", unsafe_allow_html=True)
    
    # Profile section
    with card(key="profile_card"):
        col1, col2 = st.columns([1, 3])
        
        with col1:
            # Use avatar component instead of image
            avatar(
                SITE_CONFIG.get("profile_pic", "https://via.placeholder.com/150"),
                key="profile_avatar"
            )
        
        with col2:
            st.markdown(f"# {SITE_CONFIG['author']}")
            st.markdown(f"## {SITE_CONFIG['subtitle']}")
            st.markdown("""
            Welcome to my portfolio! I'm a passionate data scientist and developer with expertise
            in machine learning, data analysis, and web development. I love solving complex problems
            and building innovative solutions.
            
            I have experience working with Python, SQL, machine learning frameworks, and web technologies.
            My goal is to leverage data to create meaningful insights and impactful applications.
            """)
            
            # Social links
            create_social_links(
                github_url=SITE_CONFIG.get("github"),
                linkedin_url=SITE_CONFIG.get("linkedin"),
                bluesky_url=SITE_CONFIG.get("bluesky"),
                key="profile",
                show_header=False,
            )
    
    # Add section anchors for navigation
    st.markdown("<div id='skills'></div>", unsafe_allow_html=True)
    
    # Skills section
    st.markdown("<h2 class='section-header'>Skills</h2>", unsafe_allow_html=True)
    
    # Prepare skills data
    skills_data = prepare_skills_data(CONTENT_CONFIG.get("skills", []))
    
    # Display skills
    display_skills(skills_data)
    
    # Add section anchors for navigation
    st.markdown("<div id='experience'></div>", unsafe_allow_html=True)
    
    # Experience section
    st.markdown("<h2 class='section-header'>Experience</h2>", unsafe_allow_html=True)
    
    # Create experience timeline
    create_timeline(
        CONTENT_CONFIG.get("experience", []),
    )
    
    # Add section anchors for navigation
    st.markdown("<div id='education'></div>", unsafe_allow_html=True)
    
    # Education section
    st.markdown("<h2 class='section-header'>Education</h2>", unsafe_allow_html=True)
    
    # Create education timeline
    create_timeline(
        CONTENT_CONFIG.get("education", []),
    )
    
    # Add section anchor for connect section
    st.markdown("<div id='connect'></div>", unsafe_allow_html=True)
    
    # Connect With Me section
    st.markdown("<h2 class='section-header'>Connect With Me</h2>", unsafe_allow_html=True)
    
    # Create social links with header
    create_social_links(
        github_url=SITE_CONFIG.get("github"),
        linkedin_url=SITE_CONFIG.get("linkedin"),
        bluesky_url=SITE_CONFIG.get("bluesky"),
        key="footer",
        show_header=True,
    )
    
    # Add JavaScript for smooth scrolling to sections
    if about_section:
        st.markdown(
            f"""
            <script>
                // Wait for the page to load
                window.addEventListener('load', function() {{
                    // Find the element with the specified ID
                    const element = document.getElementById('{about_section}');
                    
                    // If the element exists, scroll to it
                    if (element) {{
                        // Use smooth scrolling
                        element.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
                    }}
                }});
            </script>
            """,
            unsafe_allow_html=True
        )
    
    # Footer
    create_footer()


if __name__ == "__main__":
    main() 