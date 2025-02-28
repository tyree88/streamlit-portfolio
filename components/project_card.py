"""
Project card component for the Streamlit portfolio.
"""

import streamlit as st
from typing import Dict, Any, Optional, List
from streamlit_shadcn_ui import card
from streamlit_shadcn_ui import button
from streamlit_shadcn_ui.py_components.badges import badges


def create_project_card(
    project: Dict[str, Any],
    key_prefix: str = "project",
    show_creator: bool = True,
    show_buttons: bool = True,
    class_name: str = "mb-4"
) -> None:
    """
    Create a card for displaying a project using shadcn-ui.
    
    Args:
        project: Dictionary with project details
        key_prefix: Prefix for the component keys
        show_creator: Whether to show the creator badge
        show_buttons: Whether to show action buttons
        class_name: Additional CSS class names
    """
    project_key = f"{key_prefix}_{project['title'].lower().replace(' ', '_')}"
    
    with card(key=project_key, class_name=class_name):
        st.markdown(f"### {project.get('title', 'Project Title')}")
        
        # Project description
        st.markdown(project.get('description', ''))
        
        # Display tags as badges
        if 'tags' in project and project['tags']:
            st.markdown("**Technologies:**")
            badge_list = [(tag, "outline") for tag in project['tags']]
            badges(badge_list, key=f"{project_key}_tags")
        
        # Display creation info
        if show_creator and 'created_by' in project:
            creator = project['created_by']
            if creator == "Human":
                badges([("Human Made", "default")], key=f"{project_key}_creator")
            elif creator == "ChatGPT":
                badges([("ChatGPT Made", "secondary")], key=f"{project_key}_creator")
            elif creator == "Claude":
                badges([("Claude Made", "outline")], key=f"{project_key}_creator")
        
        # Display links as buttons
        if show_buttons:
            col1, col2 = st.columns(2)
            with col1:
                if 'demo_url' in project and project['demo_url']:
                    button(
                        "View Demo", 
                        variant="default", 
                        size="sm", 
                        key=f"demo_{project_key}"
                    )
            with col2:
                if 'github_url' in project and project['github_url']:
                    button(
                        "View Code", 
                        variant="outline", 
                        size="sm", 
                        key=f"code_{project_key}"
                    )


def create_featured_projects(
    projects: List[Dict[str, Any]],
    num_projects: int = 2,
    columns: int = 2,
    show_creator: bool = False
) -> None:
    """
    Create a featured projects section with multiple project cards.
    
    Args:
        projects: List of project dictionaries
        num_projects: Number of projects to display
        columns: Number of columns to display projects in
        show_creator: Whether to show the creator badge
    """
    project_cols = st.columns(columns)
    
    for i, project in enumerate(projects[:num_projects]):
        with project_cols[i % columns]:
            create_project_card(
                project,
                key_prefix="featured",
                show_creator=show_creator,
                class_name="h-full"
            ) 