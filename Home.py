"""
Main entry point for the Streamlit portfolio application.
"""

import streamlit as st
import os
from config import SITE_CONFIG
from components.footer import create_footer
from components.contact_form import create_social_links
from components.navbar import create_navbar, initialize_navigation
from streamlit_shadcn_ui import card
from streamlit_shadcn_ui import button
from streamlit_shadcn_ui.py_components.badges import badges
from utils.display_utils import load_all_css


def main():
    """Main function to render the home page."""
    # Page configuration
    st.set_page_config(
        page_title=SITE_CONFIG["title"],
        page_icon=SITE_CONFIG["icon"],
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    # Initialize navigation settings
    initialize_navigation()
    
    # Load custom CSS
    load_all_css("home")
    
    # Main content
    # Hero section with card
    with card(key="hero_card"):
        st.markdown(f"<h1 class='main-header'>{SITE_CONFIG['title']}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p class='subheader'>{SITE_CONFIG['subtitle']}</p>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(SITE_CONFIG["description"])
        with col2:
            if button("View Projects", variant="default", size="lg", key="view_projects_btn"):
                st.session_state.project_filter = "all_projects"
                st.switch_page("pages/Projects.py")
            if button("View About", variant="outline", size="lg", key="view_about_btn"):
                st.switch_page("pages/About.py")
    
    # Skills section
    st.markdown("<h2 class='section-header'>Skills & Expertise</h2>", unsafe_allow_html=True)
    
    skill_cols = st.columns(3)
    
    with skill_cols[0]:
        with card(key="data_science_card"):
            st.markdown("### Data Science")
            st.markdown("Machine Learning, Statistical Analysis, Data Visualization")
            badges([("Python", "outline"), ("Pandas", "outline"), 
                   ("Scikit-learn", "outline"), ("TensorFlow", "outline")], 
                   key="data_science_badges")
    
    with skill_cols[1]:
        with card(key="web_dev_card"):
            st.markdown("### Web Development")
            st.markdown("Full-stack development, API design, Database management")
            badges([("JavaScript", "outline"), ("React", "outline"), 
                   ("FastAPI", "outline"), ("SQL", "outline")], 
                   key="web_dev_badges")
    
    with skill_cols[2]:
        with card(key="data_eng_card"):
            st.markdown("### Data Engineering")
            st.markdown("ETL pipelines, Data warehousing, Workflow orchestration")
            badges([("Prefect", "outline"), ("Airflow", "outline"), 
                   ("SQL", "outline"), ("Docker", "outline")], 
                   key="data_eng_badges")
    
    # Featured projects section
    st.markdown("<h2 class='section-header'>Featured Projects</h2>", unsafe_allow_html=True)
    
    project_cols = st.columns(2)
    
    with project_cols[0]:
        with card(key="project1_card"):
            st.markdown("### Data Analysis Dashboard")
            st.markdown("Interactive dashboard for visualizing sales data and trends.")
            st.markdown("**Technologies:** Python, Streamlit, Pandas, Plotly")
            button("View Project", variant="default", size="sm", key="view_project1_btn")
    
    with project_cols[1]:
        with card(key="project2_card"):
            st.markdown("### Machine Learning Model")
            st.markdown("Predictive model for customer churn using ensemble methods.")
            st.markdown("**Technologies:** Python, Scikit-learn, XGBoost, Pandas")
            button("View Project", variant="default", size="sm", key="view_project2_btn")
    
    # Footer
    create_footer()


if __name__ == "__main__":
    main() 