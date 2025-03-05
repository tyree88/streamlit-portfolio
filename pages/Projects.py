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
from components.navbar import create_navbar


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
    
    # Display links as buttons in a more organized layout
    st.markdown("")  # Add some spacing
    col1, col2, col3 = st.columns([1, 1, 2])
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
        initial_sidebar_state="collapsed"
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
    
    # Navigation - same as Home.py
    create_navbar(current_page="projects")
    
    # Header with consistent styling
    st.markdown("<h1 class='main-header'>Projects</h1>", unsafe_allow_html=True)
    st.markdown("""
    <p class='subheader'>
    Explore my portfolio of projects showcasing various technologies and skills.
    Each project demonstrates different aspects of data science, machine learning, and web development.
    </p>
    """, unsafe_allow_html=True)
    
    # Load projects first - before we try to use them
    projects = load_projects()
    
    # Add created_by field if not present
    for project in projects:
        if "created_by" not in project:
            project["created_by"] = "Human"  # Default value
    
    # Main content card
    with card(key="projects_main_card"):
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
        
        # Filter section in main content
        st.markdown("<h3>Filter Options</h3>", unsafe_allow_html=True)
        
        # Create two columns for filters
        filter_col1, filter_col2 = st.columns(2)
        
        with filter_col1:
            # Extract all unique tags - now projects is defined
            all_tags = set()
            for project in projects:
                if "tags" in project:
                    all_tags.update(project["tags"])
            
            # Create filter widgets
            selected_tags = st.multiselect(
                "Technologies",
                options=sorted(list(all_tags)),
                default=[]
            )
        
        with filter_col2:
            search_term = st.text_input("Search Projects", "")
        
        # Reset filter button on its own row
        if button("Reset Filters", variant="outline", size="sm", key="reset_filters"):
            st.session_state.creation_filter = "All"
            st.experimental_rerun()
        
        # Show current active filters with badges
        active_filters = []
        if st.session_state.creation_filter != "All":
            active_filters.append((f"Creator: {st.session_state.creation_filter}", "default"))
        if selected_tags:
            active_filters.append((f"Tags: {len(selected_tags)} selected", "secondary"))
        if search_term:
            active_filters.append(("Search active", "outline"))
        
        if active_filters:
            st.markdown("**Active Filters:**")
            badges(active_filters, key="active_filters")
            st.markdown("---")  # Add a separator
        
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
        
        # Display projects with proper spacing
        if not filtered_projects:
            st.info("No projects match your filters. Try adjusting your criteria.")
        else:
            # Show number of results
            st.markdown(f"**Found {len(filtered_projects)} projects**")
            st.markdown("")  # Add spacing
            
            for project in filtered_projects:
                create_project_card(project)
                st.markdown("")  # Add spacing between cards

    # GitHub repositories section with consistent styling
    st.markdown("<h2 class='section-header'>GitHub Repositories</h2>", unsafe_allow_html=True)
    
    
    if "github" in SITE_CONFIG and SITE_CONFIG["github"]:
        github_username = SITE_CONFIG["github"].split("/")[-1]
        
        with st.spinner("Fetching GitHub repositories..."):
            try:
                repos = fetch_github_repos(github_username)
                
                if repos:
                    for repo in repos[:5]:  # Show top 5 repos
                        with card(key=f"repo_{repo['name']}"):
                            st.markdown(f"### {repo['name']}")
                            st.markdown(repo["description"] or "No description available")
                            
                            # Metrics with badges instead of columns
                            badges([
                                (f"⭐ {repo['stars']}", "default"),
                                (f"🔄 {repo['forks']}", "outline"),
                                (f"📝 {repo['language'] or 'N/A'}", "secondary")
                            ], key=f"metrics_{repo['name']}")
                            
                            st.markdown("")  # Add spacing
                            button("View Repository", variant="default", size="sm", key=f"view_repo_{repo['name']}")
                    
                    # View all repositories button
                    st.markdown("")  # Add spacing
                    button(
                        "View All Repositories",
                        variant="outline",
                        size="sm",
                        key="view_all_repos"
                    )
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