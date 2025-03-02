"""
About page for the Streamlit portfolio.
"""

import streamlit as st
from config import SITE_CONFIG, CONTENT_CONFIG
from utils.display_utils import create_timeline, display_skills
from utils.data_utils import prepare_skills_data
from components.footer import create_footer
from components.contact_form import contact_info
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
            
            # Contact buttons
            col_btn1, col_btn2, _ = st.columns([1, 1, 2])
            with col_btn1:
                button("GitHub", variant="default", size="sm", key="github_btn")
            with col_btn2:
                button("LinkedIn", variant="outline", size="sm", key="linkedin_btn")
    
    # Skills section
    st.header("Skills")
    
    with card(key="skills_card"):
        # Prepare skills data
        skills_df = prepare_skills_data(CONTENT_CONFIG["skills"])
        
        # Display skills
        display_skills(skills_df)
    
    # Experience section
    st.header("Experience")
    
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
    st.header("Education")
    
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
    st.header("Connect With Me")
    
    with card(key="contact_card"):
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
            ## Get In Touch
            
            I'm always open to discussing new projects, creative ideas, or opportunities to be part of your vision.
            
            Feel free to reach out to me through any of the social platforms listed below:
            """)
            
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
        
        with col2:
            # Contact info component
            contact_info(
                github_url=SITE_CONFIG.get("github"),
                linkedin_url=SITE_CONFIG.get("linkedin"),
                bluesky_url=SITE_CONFIG.get("bluesky"),
                key="about_page"
            )
    
    # Footer
    create_footer()


if __name__ == "__main__":
    main() 