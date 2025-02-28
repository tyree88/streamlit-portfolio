"""
Projects page for the Streamlit portfolio.
"""

import streamlit as st
import json
import os
from typing import List, Dict, Any
from config import SITE_CONFIG
from utils.github_utils import fetch_github_repos
from components.footer import create_footer
from pathlib import Path
from streamlit_shadcn_ui import card
from streamlit_shadcn_ui import button
from streamlit_shadcn_ui.py_components.badges import badges
from streamlit_shadcn_ui import tabs


# Sample projects data (in a real app, this would come from a JSON file or database)
SAMPLE_PROJECTS = [
    {
        "title": "Data Analysis Dashboard",
        "description": "Interactive dashboard for visualizing sales data and trends.",
        "tags": ["Python", "Streamlit", "Pandas", "Plotly"],
        "github_url": "https://github.com/yourusername/data-dashboard",
        "demo_url": "https://data-dashboard-demo.streamlit.app",
        "created_by": "Human"
    },
    {
        "title": "Machine Learning Model",
        "description": "Predictive model for customer churn using ensemble methods.",
        "tags": ["Python", "Scikit-learn", "XGBoost", "Pandas"],
        "github_url": "https://github.com/yourusername/churn-prediction",
        "demo_url": "",
        "created_by": "ChatGPT"
    },
    {
        "title": "Natural Language Processing App",
        "description": "Text analysis tool for sentiment analysis and entity recognition.",
        "tags": ["Python", "NLTK", "spaCy", "Streamlit"],
        "github_url": "https://github.com/yourusername/nlp-app",
        "demo_url": "https://nlp-app-demo.streamlit.app",
        "created_by": "Claude"
    }
]


def load_projects() -> List[Dict[str, Any]]:
    """
    Load projects from a JSON file or use sample data if file doesn't exist.
    
    Returns:
        List of project dictionaries
    """
    try:
        with open("data/projects.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        # Return sample projects if file not found
        return SAMPLE_PROJECTS


def create_project_card(project: Dict[str, Any]) -> None:
    """
    Create a card for displaying a project using shadcn-ui.
    
    Args:
        project: Dictionary with project details
    """
    with card(key=f"project_{project['title'].lower().replace(' ', '_')}", class_name="mb-4"):
        st.markdown(f"### {project.get('title', 'Project Title')}")
        
        # Project description
        st.markdown(project.get('description', ''))
        
        # Display tags as badges
        if 'tags' in project and project['tags']:
            st.markdown("**Technologies:**")
            badge_list = [(tag, "outline") for tag in project['tags']]
            badges(badge_list, key=f"tags_{project['title'].lower().replace(' ', '_')}")
        
        # Display creation info
        if 'created_by' in project:
            creator = project['created_by']
            if creator == "Human":
                badges([("Human Made", "default")], key=f"creator_{project['title'].lower().replace(' ', '_')}")
            elif creator == "ChatGPT":
                badges([("ChatGPT Made", "secondary")], key=f"creator_{project['title'].lower().replace(' ', '_')}")
            elif creator == "Claude":
                badges([("Claude Made", "outline")], key=f"creator_{project['title'].lower().replace(' ', '_')}")
        
        # Display links as buttons
        col1, col2 = st.columns(2)
        with col1:
            if 'demo_url' in project and project['demo_url']:
                button("View Demo", variant="default", size="sm", key=f"demo_{project['title'].lower().replace(' ', '_')}")
        with col2:
            if 'github_url' in project and project['github_url']:
                button("View Code", variant="outline", size="sm", key=f"code_{project['title'].lower().replace(' ', '_')}")


def main():
    """Main function to render the Projects page."""
    # Page configuration
    st.set_page_config(
        page_title=f"Projects | {SITE_CONFIG['title']}",
        page_icon=SITE_CONFIG["icon"],
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    # Header
    st.title("Projects")
    st.markdown("""
    Here are some of my recent projects. Each project demonstrates different skills
    and technologies. Click on the links to view the code or live demos.
    """)
    
    # Load projects
    projects = load_projects()
    
    # Add created_by field if not present
    for project in projects:
        if "created_by" not in project:
            project["created_by"] = "Human"  # Default value
    
    # Top navigation using tabs component
    tab_values = ["All", "ChatGPT Made", "Claude Made", "Human Made"]
    selected_tab = tabs(
        tab_values,
        key="project_tabs",
        default_value="All"
    )
    
    # Store the selected filter in session state
    if "creation_filter" not in st.session_state:
        st.session_state.creation_filter = selected_tab
    else:
        st.session_state.creation_filter = selected_tab
    
    # Show current filter
    st.markdown(f"**Currently showing:** {st.session_state.creation_filter} projects")
    
    # Filter options in sidebar
    st.sidebar.header("Filter Projects")
    
    # Extract all unique tags
    all_tags = set()
    for project in projects:
        if "tags" in project:
            all_tags.update(project["tags"])
    
    # Create filter widgets
    selected_tags = st.sidebar.multiselect(
        "Technologies",
        options=sorted(list(all_tags)),
        default=[]
    )
    
    search_term = st.sidebar.text_input("Search", "")
    
    # Reset creation filter button
    if st.sidebar.button("Show All Projects"):
        st.session_state.creation_filter = "All"
        st.experimental_rerun()
    
    # Filter projects
    filtered_projects = projects
    
    # Apply creation filter
    if st.session_state.creation_filter != "All":
        creation_type = st.session_state.creation_filter.replace(" Made", "")
        filtered_projects = [
            project for project in filtered_projects
            if project.get("created_by") == creation_type
        ]
    
    # Apply tag filter
    if selected_tags:
        filtered_projects = [
            project for project in filtered_projects
            if "tags" in project and any(tag in selected_tags for tag in project["tags"])
        ]
    
    # Apply search filter
    if search_term:
        search_term = search_term.lower()
        filtered_projects = [
            project for project in filtered_projects
            if search_term in project.get("title", "").lower() or 
               search_term in project.get("description", "").lower()
        ]
    
    # Display projects
    if not filtered_projects:
        st.info("No projects match your filters. Try adjusting your criteria.")
    else:
        for project in filtered_projects:
            create_project_card(project)
    
    # GitHub repositories section
    st.header("GitHub Repositories")
    
    if "github" in SITE_CONFIG and SITE_CONFIG["github"]:
        github_username = SITE_CONFIG["github"].split("/")[-1]
        
        with st.spinner("Fetching GitHub repositories..."):
            try:
                repos = fetch_github_repos(github_username)
                
                if repos:
                    for repo in repos[:5]:  # Show top 5 repos
                        with card(key=f"repo_{repo['name']}", class_name="mb-3"):
                            st.markdown(f"### {repo['name']}")
                            st.markdown(repo["description"] or "No description available")
                            
                            col1, col2, col3 = st.columns(3)
                            col1.metric("Stars", repo["stars"])
                            col2.metric("Forks", repo["forks"])
                            col3.metric("Language", repo["language"] or "N/A")
                            
                            button("View Repository", variant="default", size="sm", key=f"view_repo_{repo['name']}")
                    
                    st.markdown(f"[View all repositories]({SITE_CONFIG['github']})")
                else:
                    st.info("No GitHub repositories found.")
            except Exception as e:
                st.error(f"Error fetching GitHub repositories: {e}")
    else:
        st.info("GitHub profile not configured. Add your GitHub URL to config.py to display repositories.")
    
    # Footer
    create_footer()


if __name__ == "__main__":
    main() 