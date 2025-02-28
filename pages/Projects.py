"""
Projects page for the Streamlit portfolio.
"""

import streamlit as st
import json
import os
from typing import List, Dict, Any
from config import SITE_CONFIG
from utils.display_utils import create_project_card
from utils.github_utils import fetch_github_repos
from components.footer import create_footer
from pathlib import Path


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
    
    # Top navigation for filtering by creation method
    st.markdown("""
    <style>
    .creation-nav {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-bottom: 30px;
    }
    .creation-btn {
        background-color: #f0f2f6;
        color: #4257b2;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s;
    }
    .creation-btn.active {
        background-color: #4257b2;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        all_btn = st.button("All", key="all_btn", use_container_width=True)
    
    with col2:
        chatgpt_btn = st.button("ChatGPT Made", key="chatgpt_btn", use_container_width=True)
    
    with col3:
        claude_btn = st.button("Claude Made", key="claude_btn", use_container_width=True)
    
    with col4:
        human_btn = st.button("Human Made", key="human_btn", use_container_width=True)
    
    # Store the selected filter in session state
    if "creation_filter" not in st.session_state:
        st.session_state.creation_filter = "All"
    
    if all_btn:
        st.session_state.creation_filter = "All"
    elif chatgpt_btn:
        st.session_state.creation_filter = "ChatGPT"
    elif claude_btn:
        st.session_state.creation_filter = "Claude"
    elif human_btn:
        st.session_state.creation_filter = "Human"
    
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
        filtered_projects = [
            project for project in filtered_projects
            if project.get("created_by") == st.session_state.creation_filter
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
                        with st.container():
                            st.subheader(repo["name"])
                            st.markdown(repo["description"])
                            
                            col1, col2, col3 = st.columns(3)
                            col1.metric("Stars", repo["stars"])
                            col2.metric("Forks", repo["forks"])
                            col3.metric("Language", repo["language"] or "N/A")
                            
                            st.markdown(f"[View Repository]({repo['html_url']})")
                            st.markdown("---")
                    
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