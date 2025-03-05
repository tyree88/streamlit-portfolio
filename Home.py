"""
Main entry point for the Streamlit portfolio application.
"""

import streamlit as st
import os
from config import SITE_CONFIG
from components.footer import create_footer
from components.contact_form import create_social_links
from components.navbar import create_navbar
from streamlit_shadcn_ui import card
from streamlit_shadcn_ui import button
from streamlit_shadcn_ui.py_components.badges import badges


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


def main():
    """Main function to render the home page."""
    # Page configuration
    st.set_page_config(
        page_title=SITE_CONFIG["title"],
        page_icon=SITE_CONFIG["icon"],
        layout="wide",
        initial_sidebar_state="collapsed",
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
    
    # Navigation
    create_navbar(current_page="home")
    
    # Main content
    # Hero section with card
    with card(key="hero_card"):
        st.markdown(f"<h1 class='main-header'>{SITE_CONFIG['title']}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p class='subheader'>{SITE_CONFIG['subtitle']}</p>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(SITE_CONFIG["description"])
        with col2:
            button("View Projects", variant="default", size="lg", class_name="w-full mb-2", key="view_projects_btn")
            if button("View About", variant="outline", size="lg", class_name="w-full", key="view_about_btn"):
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