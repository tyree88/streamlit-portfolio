"""
About page for the Streamlit portfolio.
"""

import streamlit as st
from config import SITE_CONFIG, CONTENT_CONFIG
from utils.display_utils import create_timeline, display_skills
from utils.data_utils import prepare_skills_data
from components.footer import create_footer
from components.contact_form import create_social_links
from components.navbar import create_navbar
from streamlit_shadcn_ui import card
from streamlit_shadcn_ui import button
from streamlit_shadcn_ui.py_components.badges import badges
from streamlit_shadcn_ui import avatar
import os


def load_css():
    """Load custom CSS."""
    css_file = "assets/css/style.css"
    if os.path.exists(css_file):
        with open(css_file) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    else:
        # Default styling if CSS file doesn't exist
        st.markdown("""
        <style>
        /* Dark theme styling */
        :root {
            --background-color: #121212;
            --text-color: #ffffff;
            --accent-color: #0285FF;
            --secondary-color: #333333;
            --card-bg-color: #1e1e1e;
            --hover-color: #2a2a2a;
            --border-color: #333333;
        }
        
        body {
            color: var(--text-color);
            background-color: var(--background-color);
        }
        
        /* Full width content */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 100% !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
        
        /* Remove default padding */
        .css-18e3th9 {
            padding-top: 0 !important;
            padding-right: 0 !important;
            padding-left: 0 !important;
            padding-bottom: 0 !important;
        }
        
        /* Remove container width restrictions */
        .css-1n76uvr, .css-1vq4p4l {
            max-width: 100% !important;
        }
        
        .main-header {
            font-size: 2.5rem;
            margin-bottom: 1rem;
            color: var(--text-color);
        }
        
        .subheader {
            font-size: 1.5rem;
            color: var(--accent-color);
            margin-bottom: 2rem;
        }
        
        .section-header {
            font-size: 1.8rem;
            margin-top: 2rem;
            margin-bottom: 1rem;
            color: var(--text-color);
        }
        
        .highlight {
            background-color: var(--card-bg-color);
            padding: 1.5rem;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
        }
        
        /* Streamlit specific overrides */
        .stApp {
            background-color: var(--background-color);
        }
        
        .stButton > button {
            background-color: var(--accent-color);
            color: white;
        }
        
        [data-testid="stVerticalBlock"] [data-testid="stHorizontalBlock"] > div > div[data-testid="stVerticalBlock"] {
            background-color: var(--card-bg-color);
            border: 1px solid var(--border-color);
        }
        
        /* Hide sidebar collapse control */
        [data-testid="collapsedControl"] {
            display: none
        }
        </style>
        """, unsafe_allow_html=True)

def profile_card_content():
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
                    show_description=False
                )
def main():
    """Main function to render the About page."""
    # Page configuration
    st.set_page_config(
        page_title=f"About | {SITE_CONFIG['title']}",
        page_icon=SITE_CONFIG["icon"],
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Hide sidebar completely
    st.markdown(
        """
    <style>
        [data-testid="collapsedControl"] {
            display: none
        }
    </style>
    """,
        unsafe_allow_html=True,
    )
    
    # Load custom CSS
    load_css()
    
    # Navigation - same as Home.py
    create_navbar(current_page="about")
    
    # Header
    st.title("About Me")
    
    # Profile section
    card(key="profile_card",content=profile_card_content(),title="Profile",description="Profile",)
        
        
        # profile_card_content()
    # Skills section
    st.markdown("<h2 class='section-header'>Skills</h2>", unsafe_allow_html=True)
    
    # Prepare skills data
    skills_df = prepare_skills_data(CONTENT_CONFIG["skills"])
    
    # Display skills
    display_skills(skills_df)
    
    # Experience section
    st.markdown("<h2 class='section-header'>Experience</h2>", unsafe_allow_html=True)
    
    with card(key="experience_card"):
        for i, experience in enumerate(CONTENT_CONFIG["experience"]):
            col1, col2 = st.columns([1, 3])
            
            with col1:
                st.markdown(f"**{experience.get('period', '')}**")
                badges([(experience.get('company', ''), "outline")], 
                       key=f"company_{i}")
            
            with col2:
                st.markdown(f"### {experience.get('title', '')}")
                st.markdown(experience.get('description', ''))
            
            if i < len(CONTENT_CONFIG["experience"]) - 1:
                st.markdown("---")
    
    # Education section
    st.markdown("<h2 class='section-header'>Education</h2>", unsafe_allow_html=True)
    
    with card(key="education_card"):
        for i, education in enumerate(CONTENT_CONFIG["education"]):
            col1, col2 = st.columns([1, 3])
            
            with col1:
                st.markdown(f"**{education.get('year', '')}**")
                badges([(education.get('institution', ''), "outline")], 
                       key=f"institution_{i}")
            
            with col2:
                st.markdown(f"### {education.get('degree', '')}")
                st.markdown(education.get('description', ''))
            
            if i < len(CONTENT_CONFIG["education"]) - 1:
                st.markdown("---")
    
    # Contact section
    st.markdown("<h2 class='section-header'>Connect With Me</h2>", unsafe_allow_html=True)
    
    with card(key="contact_card"):
        st.markdown("""
        ## Get In Touch
        
        I'm always open to discussing new projects, creative ideas, or opportunities to be part of your vision.
        Feel free to connect with me on social media to discuss projects or just to network!
        """)
        
        create_social_links(
            github_url=SITE_CONFIG.get("github"),
            linkedin_url=SITE_CONFIG.get("linkedin"),
            bluesky_url=SITE_CONFIG.get("bluesky"),
            key="contact"
        )
    
    # Footer
    create_footer()


if __name__ == "__main__":
    main() 