"""
About page for the Streamlit portfolio.
"""

import streamlit as st
from config import SITE_CONFIG, CONTENT_CONFIG
from utils.display_utils import create_timeline, display_skills
from utils.data_utils import prepare_skills_data
from components.footer import create_footer


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
    col1, col2 = st.columns([2, 3])
    
    # with col1:
    #     st.image("assets/images/profile.jpg", width=300)
    
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
        col_btn1.markdown(f"[![GitHub](https://img.shields.io/badge/GitHub-Profile-blue?style=for-the-badge&logo=github)]({SITE_CONFIG['github']})")
        col_btn2.markdown(f"[![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-blue?style=for-the-badge&logo=linkedin)]({SITE_CONFIG['linkedin']})")
    
    # Skills section
    st.header("Skills")
    
    # Prepare skills data
    skills_df = prepare_skills_data(CONTENT_CONFIG["skills"])
    
    # Display skills
    display_skills(skills_df)
    
    # Experience section
    st.header("Experience")
    create_timeline(CONTENT_CONFIG["experience"])
    
    # Education section
    st.header("Education")
    create_timeline(CONTENT_CONFIG["education"])
    
    # Footer
    create_footer()


if __name__ == "__main__":
    main() 