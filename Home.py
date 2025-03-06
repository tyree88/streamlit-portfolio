"""
Main entry point for the Streamlit portfolio application.
"""

import streamlit as st
import os
from config import SITE_CONFIG
from components.footer import create_footer
from components.social_links import create_social_links
from components.navbar import create_navbar, initialize_navigation
import streamlit_shadcn_ui as ui
import streamlit_antd_components as sac
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
    
    # Hero section with modern card
    with ui.card(key="hero_card"):
        ui.element("h1", children=[SITE_CONFIG['title']], className="text-3xl font-bold tracking-tight", key="hero_title")
        ui.element("p", children=[SITE_CONFIG['subtitle']], className="text-xl text-gray-400 mt-2", key="hero_subtitle")
        ui.element("p", children=[SITE_CONFIG["description"]], className="mt-4 text-gray-300 mb-4", key="hero_description")
        
        # Button container
        ui.element("div", children=[], className="flex gap-4 mt-6", key="hero_buttons_container")
        
        # Initialize button selection state if not exists
        if "hero_nav_selection" not in st.session_state:
            st.session_state.hero_nav_selection = None
        

    
    
    # Featured Projects section with modern project cards
    st.markdown("<h2 class='section-title'>Featured Projects</h2>", unsafe_allow_html=True)
    
    # Create a 2-column layout for projects
    project_cols = st.columns(2)
    
    # Data Analysis Dashboard project card
    with project_cols[0]:
        with ui.card(key="project1_card"):
            # Project header
            ui.element("h3", children=["Data Analysis Dashboard"], className="text-xl font-bold", key="p1_title")
            ui.element("p", children=["Interactive dashboard for visualizing sales data and trends."], 
                      className="text-gray-400 mt-2", key="p1_desc")
            
            
            
            # Technologies using sac.chip
            ui.element("p", children=["Technologies:"], className="text-sm text-gray-400 mb-2", key="p1_tech_label")
            sac.chip(
                items=[
                    sac.ChipItem(label='Python'),
                    sac.ChipItem(label='Streamlit'),
                    sac.ChipItem(label='Pandas'),
                    sac.ChipItem(label='Plotly'),
                ],
                index=[0, 1, 2, 3],
                radius='md',
                color='blue',
                variant='light',
                multiple=True,
                key="p1_chips"
            )
            
            # Use sac.buttons for project link
            sac.buttons([
                sac.ButtonsItem(label='View Project', icon='folder-fill', color='#333333',href="pages/Projects.py"),
            ], align='center', key='project1_nav_button')
    
    # Machine Learning Model project card
    with project_cols[1]:
        with ui.card(key="project2_card"):
            # Project header
            ui.element("h3", children=["Machine Learning Model"], className="text-xl font-bold", key="p2_title")
            ui.element("p", children=["Predictive model for customer churn using ensemble methods."], 
                      className="text-gray-400 mt-2", key="p2_desc")
            

            
            # Technologies using sac.chip
            ui.element("p", children=["Technologies:"], className="text-sm text-gray-400 mb-2", key="p2_tech_label")
            sac.chip(
                items=[
                    sac.ChipItem(label='Python'),
                    sac.ChipItem(label='Scikit-learn'),
                    sac.ChipItem(label='XGBoost'),
                    sac.ChipItem(label='Pandas'),
                ],
                index=[0, 1, 2, 3],
                radius='md',
                color='green',
                variant='light',
                multiple=True,
                key="p2_chips"
            )
            
            # Use sac.buttons for project link
            sac.buttons([
                sac.ButtonsItem(label='View Project', icon='folder-fill', color='#333333',href="pages/Projects.py"),
            ], align='center', key='project2_nav_button')
            
    
    # Footer with modern styling
    create_footer()


if __name__ == "__main__":
    main() 