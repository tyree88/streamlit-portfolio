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
from components.navbar import create_navbar, initialize_navigation
from utils.display_utils import load_css_file


def load_css():
    """Load CSS files for the Projects page."""
    # Load common CSS
    load_css_file("assets/css/pages/common.css")
    # Load page-specific CSS
    load_css_file("assets/css/pages/projects.css")


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
    Load projects from a JSON file or use sample data.
    
    Returns:
        List of project dictionaries
    """
    # Try to load from a JSON file first
    projects_file = Path("data/projects.json")
    if projects_file.exists():
        try:
            with open(projects_file, "r") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Error loading projects: {e}")
    
    # Fall back to sample data
    return SAMPLE_PROJECTS


def create_project_card(project: Dict[str, Any]) -> None:
    """
    Create a card for a single project.
    
    Args:
        project: Dictionary containing project details
    """
    with card(key=f"project_{project['title'].lower().replace(' ', '_')}"):
        st.markdown(f"### {project['title']}")
        st.markdown(project["description"])
        
        # Display tags as badges
        if "tags" in project and project["tags"]:
            tag_badges = [(tag, "default") for tag in project["tags"]]
            badges(tag_badges, key=f"tags_{project['title'].lower().replace(' ', '_')}")
        
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


def setup_page():
    """Set up the page configuration and load necessary resources."""
    # Page configuration
    st.set_page_config(
        page_title=f"Projects | {SITE_CONFIG['title']}",
        page_icon=SITE_CONFIG["icon"],
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize navigation settings
    initialize_navigation()
    
    # Load custom CSS
    load_css()
    
    # Header with consistent styling
    st.markdown("<h1 class='main-header'>Projects</h1>", unsafe_allow_html=True)


def display_filter_header(project_filter):
    """Display the appropriate header based on the current filter."""
    if project_filter == "data_science":
        st.markdown("""
        <p class='subheader'>
        Data Science Projects - Explore my portfolio of data analysis and visualization projects.
        </p>
        """, unsafe_allow_html=True)
    elif project_filter == "web_dev":
        st.markdown("""
        <p class='subheader'>
        Web Development Projects - Explore my portfolio of web applications and sites.
        </p>
        """, unsafe_allow_html=True)
    elif project_filter == "ml":
        st.markdown("""
        <p class='subheader'>
        Machine Learning Projects - Explore my portfolio of ML models and applications.
        </p>
        """, unsafe_allow_html=True)
    elif project_filter == "github_repos":
        st.markdown("""
        <p class='subheader'>
        GitHub Repositories - Explore my open-source contributions and personal projects on GitHub.
        </p>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <p class='subheader'>
        Explore my portfolio of projects showcasing various technologies and skills.
        Each project demonstrates different aspects of data science, machine learning, and web development.
        </p>
        """, unsafe_allow_html=True)


def prepare_projects(projects):
    """
    Prepare projects by ensuring they have required fields and categorizing them.
    
    Args:
        projects: List of project dictionaries
    
    Returns:
        List of prepared project dictionaries
    """
    for project in projects:
        # Ensure created_by field
        if "created_by" not in project:
            project["created_by"] = "Human"
        
        # Assign category based on tags
        if "category" not in project:
            tags = project.get("tags", [])
            if any(tag in ["Data Analysis", "Pandas", "Tableau", "Power BI", "SQL"] for tag in tags):
                project["category"] = "data_science"
            elif any(tag in ["React", "JavaScript", "HTML", "CSS", "Web", "Frontend", "Backend"] for tag in tags):
                project["category"] = "web_dev"
            elif any(tag in ["Machine Learning", "Deep Learning", "AI", "Neural Networks", "TensorFlow", "PyTorch"] for tag in tags):
                project["category"] = "ml"
            else:
                project["category"] = "other"
    
    return projects


def display_github_repos():
    """Display GitHub repositories section."""
    from components.github_repo_card import create_github_repos_section
    from utils.github_utils import fetch_github_repos
    
    # Get GitHub username from config
    github_username = SITE_CONFIG.get("github", "").split("/")[-1]
    
    if github_username:
        # Fetch GitHub repositories
        repos = fetch_github_repos(github_username)
        
        # Display GitHub repositories
        create_github_repos_section(repos, max_repos=10, show_view_all=True, github_url=SITE_CONFIG.get("github"))
    else:
        st.warning("GitHub username not configured. Please add your GitHub username to the config file.")
    
    # Add a footer
    st.markdown("---")
    st.markdown("### Want to see more projects?")
    st.markdown("Check out the other project categories in the navigation menu.")


def setup_filter_ui(projects):
    """
    Set up the filter UI components.
    
    Args:
        projects: List of project dictionaries
    
    Returns:
        Tuple containing (selected_tab, selected_tags, search_term)
    """
    # Create tabs for filtering by creator type
    creator_tabs = ["All", "ChatGPT Made", "Claude Made", "Human Made", "AI Assisted"]
    
    # Check if we have a creation filter from the navbar
    creation_filter = st.session_state.get("creation_filter", "All")
    
    # Handle the AI Assisted filter which is a custom filter
    if creation_filter == "AI Assisted" and "AI Assisted" not in creator_tabs:
        # If AI Assisted is not in the tabs, use the closest match
        selected_tab = "ChatGPT Made"  # Default fallback
    else:
        # Use the tabs component for creator filtering
        selected_tab = tabs(
            creator_tabs,
            key="project_tabs",
            default_value=creation_filter
        )
    
    # Store the selected filter in session state
    st.session_state.creation_filter = selected_tab

    # Filter section in main content
    st.markdown("<h3>Filter Options</h3>", unsafe_allow_html=True)
    
    # Create two columns for filters
    filter_col1, filter_col2 = st.columns(2)
    
    with filter_col1:
        # Extract all unique tags
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
        
        # Check if we should focus on the technology filter
        if st.session_state.get("focus_on_tech_filter", False):
            # Clear the flag so it doesn't persist
            st.session_state.focus_on_tech_filter = False
            # Add a note to guide the user
            st.info("Select technologies above to filter projects by specific tools or languages.")
    
    with filter_col2:
        search_term = st.text_input("Search Projects", "")
    
    # Reset filter button on its own row
    if button("Reset Filters", variant="outline", size="sm", key="reset_filters"):
        st.session_state.creation_filter = "All"
        st.session_state.project_filter = None
        st.session_state.focus_on_tech_filter = False
        st.rerun()
    
    # Show current active filters with badges
    display_active_filters(selected_tab, selected_tags, search_term)
    
    return selected_tab, selected_tags, search_term


def display_active_filters(selected_tab, selected_tags, search_term):
    """Display badges for active filters."""
    active_filters = []
    if selected_tab != "All":
        active_filters.append((f"Creator: {selected_tab}", "default"))
    if selected_tags:
        active_filters.append((f"Tags: {len(selected_tags)} selected", "secondary"))
    if search_term:
        active_filters.append(("Search active", "outline"))
    
    if active_filters:
        st.markdown("**Active Filters:**")
        badges(active_filters, key="active_filters")
        st.markdown("---")  # Add a separator


def filter_projects(projects, selected_tab, selected_tags, search_term, project_filter):
    """
    Filter projects based on selected criteria.
    
    Args:
        projects: List of project dictionaries
        selected_tab: Selected creator tab
        selected_tags: List of selected technology tags
        search_term: Search term for filtering
        project_filter: Category filter from the navbar
    
    Returns:
        List of filtered project dictionaries
    """
    filtered_projects = []
    for project in projects:
        # Filter by creator type
        if selected_tab != "All":
            if selected_tab == "AI Assisted":
                # Show both ChatGPT and Claude made projects
                if project.get("created_by") not in ["ChatGPT", "Claude"]:
                    continue
            elif selected_tab != project.get("created_by"):
                continue
        
        # Filter by category if set from navbar
        if project_filter and project_filter not in ["all_projects", "github_repos"]:
            if project.get("category") != project_filter:
                continue
        
        # Filter by tags
        if selected_tags and not any(tag in project.get("tags", []) for tag in selected_tags):
            continue
        
        # Filter by search term
        if search_term:
            search_term_lower = search_term.lower()
            title = project.get("title", "").lower()
            description = project.get("description", "").lower()
            tags = [tag.lower() for tag in project.get("tags", [])]
            
            if (search_term_lower not in title and 
                search_term_lower not in description and 
                not any(search_term_lower in tag for tag in tags)):
                continue
        
        filtered_projects.append(project)
    
    return filtered_projects


def display_projects(filtered_projects):
    """
    Display the filtered projects.
    
    Args:
        filtered_projects: List of filtered project dictionaries
    """
    if not filtered_projects:
        st.info("No projects match your filters. Try adjusting your criteria.")
    else:
        # Show number of results
        st.markdown(f"**Found {len(filtered_projects)} projects**")
        st.markdown("")  # Add spacing
        
        for project in filtered_projects:
            create_project_card(project)
            st.markdown("")  # Add spacing between cards


def main():
    """Main function to render the Projects page."""
    # Set up the page
    setup_page()

    # Check if we have a project filter from the navbar
    project_filter = st.session_state.get("project_filter", "all_projects")
    
    # Debug information
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Debug Info")
    st.sidebar.write(f"Current filter: {project_filter}")

    # Display appropriate header based on filter
    display_filter_header(project_filter)

    # Load and prepare projects
    projects = load_projects()
    projects = prepare_projects(projects)
    
    # Handle GitHub repos filter separately
    if project_filter == "github_repos":
        display_github_repos()
        # Initialize filtered_projects as empty list for GitHub repos case
        filtered_projects = []
    else:
        # Main content card with tabs for filtering
        with card(key="projects_main_card"):
            # Set up filter UI
            selected_tab, selected_tags, search_term = setup_filter_ui(projects)
            
            # Filter projects based on criteria
            filtered_projects = filter_projects(
                projects, 
                selected_tab, 
                selected_tags, 
                search_term, 
                project_filter
            )
            
            # Display filtered projects
            display_projects(filtered_projects)

    # Footer
    create_footer()


if __name__ == "__main__":
    main() 