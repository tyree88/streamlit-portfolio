"""
Display utility functions for the Streamlit portfolio.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt
from typing import List, Dict, Any
import os.path


def display_skills(skills_df: pd.DataFrame) -> None:
    """
    Display skills as a horizontal bar chart.
    
    Args:
        skills_df: DataFrame with skills data (name, level, category)
    """
    # Create a horizontal bar chart with Plotly
    fig = px.bar(
        skills_df,
        x='level',
        y='name',
        color='category',
        orientation='h',
        title='Skills',
        labels={'level': 'Proficiency', 'name': ''},
        color_discrete_map={
            'Advanced': '#4257b2',
            'Intermediate': '#5c88da',
            'Beginner': '#a3b9ef'
        },
        height=400
    )
    
    # Customize the layout
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_size=12,
        margin=dict(l=0, r=0, t=40, b=0),
        xaxis=dict(range=[0, 100])
    )
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True)


def create_timeline(events: List[Dict[str, Any]]) -> None:
    """
    Create a timeline visualization for events like education or work experience.
    
    Args:
        events: List of event dictionaries with 'title', 'period', and 'description'
    """
    for i, event in enumerate(events):
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown(f"**{event.get('period', '')}**")
        
        with col2:
            st.markdown(f"### {event.get('title', '')}")
            st.markdown(f"*{event.get('company', event.get('institution', ''))}*")
            st.markdown(event.get('description', ''))
        
        if i < len(events) - 1:
            st.markdown("---")


def create_project_card(project: Dict[str, Any]) -> None:
    """
    Create a card for displaying a project.
    
    Args:
        project: Dictionary with project details
    """
    with st.container():
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Instead of trying to load potentially missing images, use a placeholder
            st.markdown(f"### {project.get('title', 'Project Title')}")
            # Display a colored box instead of an image
            st.markdown(
                f"""
                <div style="
                    background-color: #4257b2; 
                    height: 150px; 
                    border-radius: 10px; 
                    display: flex; 
                    align-items: center; 
                    justify-content: center;
                    color: white;
                    font-weight: bold;
                ">
                    {project.get('title', 'Project')}
                </div>
                """, 
                unsafe_allow_html=True
            )
        
        with col2:
            st.markdown(project.get('description', ''))
            
            # Display tags
            if 'tags' in project and project['tags']:
                st.markdown("**Technologies:**")
                tags_html = " ".join([
                    f'<span style="background-color: #e9ecef; padding: 3px 8px; '
                    f'border-radius: 10px; margin-right: 5px; font-size: 0.8rem;">{tag}</span>'
                    for tag in project['tags']
                ])
                st.markdown(tags_html, unsafe_allow_html=True)
            
            # Display links
            cols = st.columns(2)
            if 'demo_url' in project and project['demo_url']:
                cols[0].markdown(f"[View Demo]({project['demo_url']})")
            if 'github_url' in project and project['github_url']:
                cols[1].markdown(f"[View Code]({project['github_url']})")
        
        st.markdown("---")


def load_css_file(css_file_path: str) -> None:
    """
    Load a CSS file and inject it into the Streamlit app.
    
    Args:
        css_file_path: Path to the CSS file relative to the application root
    """
    import streamlit as st
    import os
    
    # Try to find the file at the given path
    if os.path.exists(css_file_path):
        with open(css_file_path) as f:
            css_content = f.read()
            # Wrap CSS in style tags and inject it
            st.markdown(f'<style>{css_content}</style>', unsafe_allow_html=True)
    else:
        # If not found, try to find it relative to the current file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(current_dir, "../.."))
        absolute_path = os.path.join(project_root, css_file_path)
        
        if os.path.exists(absolute_path):
            with open(absolute_path) as f:
                css_content = f.read()
                # Wrap CSS in style tags and inject it
                st.markdown(f'<style>{css_content}</style>', unsafe_allow_html=True)
        else:
            st.warning(f"CSS file not found: {css_file_path}")
            st.info(f"Tried paths: \n1. {css_file_path}\n2. {absolute_path}")


def load_all_css(page_name: str = None) -> None:
    """
    Load all necessary CSS files for the application.
    
    Args:
        page_name: Optional name of the current page to load page-specific CSS
    """
    import streamlit as st
    
    # Load common CSS first
    load_css_file("assets/css/pages/common.css")
    
    # Load page-specific CSS if provided
    if page_name and page_name.lower() in ["home", "about", "projects"]:
        load_css_file(f"assets/css/pages/{page_name.lower()}.css") 