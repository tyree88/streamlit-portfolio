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


def main():
    """Main function to render the About page."""
    # Page configuration
    st.set_page_config(
        page_title=f"About | {SITE_CONFIG['title']}",
        page_icon=SITE_CONFIG["icon"],
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    # Navigation
    create_navbar(current_page="about")
    
    # Header
    st.title("About Me")
    
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
                show_description=False
            )
    
    # Skills section
    st.markdown("<h2 class='section-header'>Skills</h2>", unsafe_allow_html=True)
    
    with card(key="skills_card"):
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