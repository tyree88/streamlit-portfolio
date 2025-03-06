"""
Projects page for the Streamlit portfolio.
"""

import streamlit as st
import json
import os
import sys
from typing import List, Dict, Any
from pathlib import Path

# Add parent directory to path to import config
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
try:
    from config import SITE_CONFIG
except ImportError:
    # Fallback config if import fails
    SITE_CONFIG = {
        "github_username": "",
        "site_title": "Portfolio",
        "site_description": "My Portfolio"
    }

from utils.github_utils import fetch_github_repos
from components.footer import create_footer
import streamlit_shadcn_ui as ui
import streamlit_antd_components as sac
from components.navbar import create_navbar, initialize_navigation
from utils.display_utils import load_all_css


def load_css():
    """Load CSS files for the Projects page."""
    # Load all CSS files
    load_all_css("projects")


# Sample projects data (in a real app, this would come from a JSON file or database)
SAMPLE_PROJECTS = [
    {
        "title": "Data Analysis Dashboard",
        "description": "Interactive dashboard for visualizing sales data and trends.",
        "tags": ["Python", "Streamlit", "Pandas", "Plotly", "Data Science", "Data Analysis", "Visualization"],
        "github_url": "https://github.com/yourusername/data-dashboard",
        "demo_url": "https://data-dashboard-demo.streamlit.app",
        "created_by": "Human"
    },
    {
        "title": "Machine Learning Model",
        "description": "Predictive model for customer churn using ensemble methods.",
        "tags": ["Python", "Scikit-learn", "XGBoost", "Pandas", "Machine Learning", "Data Science"],
        "github_url": "https://github.com/yourusername/churn-prediction",
        "demo_url": "",
        "created_by": "ChatGPT"
    },
    {
        "title": "Natural Language Processing App",
        "description": "Text analysis tool for sentiment analysis and entity recognition.",
        "tags": ["Python", "NLTK", "spaCy", "Streamlit", "Machine Learning", "NLP"],
        "github_url": "https://github.com/yourusername/nlp-app",
        "demo_url": "https://nlp-app-demo.streamlit.app",
        "created_by": "Claude"
    },
    {
        "title": "Personal Portfolio Website",
        "description": "Modern portfolio website built with React and Tailwind CSS.",
        "tags": ["JavaScript", "React", "Tailwind CSS", "HTML", "CSS", "Web Development"],
        "github_url": "https://github.com/yourusername/portfolio",
        "demo_url": "https://yourusername.github.io/portfolio",
        "created_by": "Human"
    },
    {
        "title": "E-commerce Platform",
        "description": "Full-stack e-commerce platform with user authentication and payment processing.",
        "tags": ["JavaScript", "React", "Node.js", "Express", "MongoDB", "Web Development"],
        "github_url": "https://github.com/yourusername/ecommerce",
        "demo_url": "https://ecommerce-demo.herokuapp.com",
        "created_by": "Human"
    },
    {
        "title": "Deep Learning Image Classifier",
        "description": "Convolutional neural network for image classification trained on custom dataset.",
        "tags": ["Python", "TensorFlow", "Keras", "Deep Learning", "Machine Learning", "Computer Vision"],
        "github_url": "https://github.com/yourusername/image-classifier",
        "demo_url": "https://huggingface.co/spaces/yourusername/image-classifier",
        "created_by": "ChatGPT"
    },
    {
        "title": "API Development Framework",
        "description": "Lightweight framework for building RESTful APIs with authentication and rate limiting.",
        "tags": ["Python", "FastAPI", "SQLAlchemy", "Web Development", "API"],
        "github_url": "https://github.com/yourusername/api-framework",
        "demo_url": "https://api-framework-docs.netlify.app",
        "created_by": "Human"
    },
    {
        "title": "Time Series Forecasting Tool",
        "description": "Advanced time series forecasting tool using ARIMA, Prophet, and LSTM models.",
        "tags": ["Python", "Pandas", "Statsmodels", "Prophet", "TensorFlow", "Data Science", "Machine Learning"],
        "github_url": "https://github.com/yourusername/time-series",
        "demo_url": "https://time-series-demo.streamlit.app",
        "created_by": "Claude"
    },
    {
        "title": "Mobile App with React Native",
        "description": "Cross-platform mobile app for task management with cloud synchronization.",
        "tags": ["JavaScript", "React Native", "Firebase", "Mobile Development", "Web Development"],
        "github_url": "https://github.com/yourusername/task-app",
        "demo_url": "",
        "created_by": "Human"
    },
    {
        "title": "Recommendation System",
        "description": "Content-based and collaborative filtering recommendation system for movies.",
        "tags": ["Python", "Pandas", "Scikit-learn", "Machine Learning", "Data Science"],
        "github_url": "https://github.com/yourusername/movie-recommender",
        "demo_url": "https://movie-recommender-demo.streamlit.app",
        "created_by": "ChatGPT"
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


def create_project_card(project: Dict[str, Any], index: int) -> None:
    """
    Create a card for a project.
    
    Args:
        project: Project data
        index: Index of the project
    """
    project_id = f"project_{index}"
    
    with ui.card(key=f"{project_id}_card"):
        # Project header section
        ui.element("div", 
                  children=[], 
                  className="project-header", 
                  key=f"{project_id}_header")
        
        # Project title with icon
        # Handle both GitHub repos (name) and sample projects (title)
        project_title = project.get('name') if 'name' in project else project.get('title', 'Untitled Project')
        ui.element("h3", 
                  children=[project_title], 
                  className="project-title", 
                  key=f"{project_id}_title")
        
        # Project description
        ui.element("p", 
                  children=[project.get('description', 'No description available.')], 
                  className="project-description", 
                  key=f"{project_id}_desc")
        
        # Visual element placeholder (image or icon)
        ui.element("div", 
                  children=[], 
                  className="project-visual-placeholder", 
                  key=f"{project_id}_visual")
        
        # Project metadata section
        ui.element("div", 
                  children=[], 
                  className="project-metadata", 
                  key=f"{project_id}_metadata")
        
        # Tags as chips - handle both GitHub topics and sample project tags
        tags = project.get('topics', project.get('tags', []))
        if tags:
            st.write("##### Technologies")
            
            chip_items = [sac.ChipItem(label=tag) for tag in tags]
            sac.chip(
                items=chip_items,
                index=None,
                align="start",
                size="sm",
                radius="md",
                variant="light",
                color="blue",
                multiple=False,
                key=f"{project_id}_tags"
            )
        
        # Project stats section
        st.markdown("---")
        
        # Create a flex container for the project stats
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            # Language badge - handle both GitHub language and sample project tags
            language = project.get('language', None)
            if not language and tags:
                # Try to find a language in the tags
                common_languages = ['Python', 'JavaScript', 'TypeScript', 'Java', 'C#', 'HTML', 'CSS', 'Go', 'Ruby']
                for lang in common_languages:
                    if lang in tags:
                        language = lang
                        break
            
            if language:
                lang_color = {
                    'Python': 'blue',
                    'JavaScript': 'yellow',
                    'TypeScript': 'blue',
                    'Java': 'orange',
                    'C#': 'green',
                    'HTML': 'red',
                    'CSS': 'purple'
                }.get(language, 'gray')
                
                st.markdown(f"<span class='language-badge' style='background-color: var(--{lang_color}-500);'>{language}</span>", unsafe_allow_html=True)
        
        with col2:
            # Stars count - GitHub specific
            stars = project.get('stars', 0)
            st.markdown(f"<div class='stat-item'><span class='stat-icon'>⭐</span> <span class='stat-value'>{stars}</span></div>", unsafe_allow_html=True)
        
        with col3:
            # Forks count - GitHub specific
            forks = project.get('forks', 0)
            st.markdown(f"<div class='stat-item'><span class='stat-icon'>🍴</span> <span class='stat-value'>{forks}</span></div>", unsafe_allow_html=True)
        
        # Creation info
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        # Handle both GitHub dates and sample project created_by
        with col1:
            if 'created_at' in project:
                created_at = project.get('created_at', 'Unknown')
                st.markdown(f"<div class='date-info'><span class='date-label'>Created:</span> <span class='date-value'>{created_at}</span></div>", unsafe_allow_html=True)
            elif 'created_by' in project:
                created_by = project.get('created_by', 'Unknown')
                st.markdown(f"<div class='date-info'><span class='date-label'>Created by:</span> <span class='date-value'>{created_by}</span></div>", unsafe_allow_html=True)
        
        with col2:
            if 'updated_at' in project:
                updated_at = project.get('updated_at', 'Unknown')
                st.markdown(f"<div class='date-info'><span class='date-label'>Updated:</span> <span class='date-value'>{updated_at}</span></div>", unsafe_allow_html=True)
        
        # Action buttons
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            # Handle both GitHub homepage and sample project demo_url
            demo_url = project.get('homepage', project.get('demo_url', ''))
            if demo_url:
                st.button(
                    "🚀 View Demo", 
                    key=f"{project_id}_demo_btn",
                    use_container_width=True,
                    on_click=lambda: st.session_state.update({f"{project_id}_demo_url": demo_url})
                )
                
                # Open URL if button was clicked
                if st.session_state.get(f"{project_id}_demo_url"):
                    st.markdown(f'<script>window.open("{st.session_state[f"{project_id}_demo_url"]}", "_blank");</script>', unsafe_allow_html=True)
                    # Reset the state
                    st.session_state[f"{project_id}_demo_url"] = None
        
        with col2:
            # Handle both GitHub html_url and sample project github_url
            github_url = project.get('html_url', project.get('github_url', ''))
            if github_url:
                st.button(
                    "💻 View Code", 
                    key=f"{project_id}_code_btn",
                    use_container_width=True,
                    on_click=lambda: st.session_state.update({f"{project_id}_code_url": github_url})
                )
                
                # Open URL if button was clicked
                if st.session_state.get(f"{project_id}_code_url"):
                    st.markdown(f'<script>window.open("{st.session_state[f"{project_id}_code_url"]}", "_blank");</script>', unsafe_allow_html=True)
                    # Reset the state
                    st.session_state[f"{project_id}_code_url"] = None


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
        selected_tab = sac.tabs(
            items=[sac.TabsItem(label=tab) for tab in creator_tabs],
            index=creator_tabs.index(creation_filter) if creation_filter in creator_tabs else 0,
            key="project_filter_tabs"
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
            default=[],
            key="project_tech_filter"
        )
        
        # Check if we should focus on the technology filter
        if st.session_state.get("focus_on_tech_filter", False):
            # Clear the flag so it doesn't persist
            st.session_state.focus_on_tech_filter = False
            # Add a note to guide the user
            st.info("Select technologies above to filter projects by specific tools or languages.")
    
    with filter_col2:
        search_term = st.text_input("Search Projects", "", key="project_search_filter")
    
    # Reset filter button on its own row
    if ui.button("Reset Filters", variant="outline", size="sm", key="reset_filters_btn"):
        st.session_state.creation_filter = "All"
        st.session_state.project_filter = None
        st.session_state.focus_on_tech_filter = False
        st.rerun()
    
    # Show current active filters with chips
    display_active_filters(selected_tab, selected_tags, search_term)
    
    return selected_tab, selected_tags, search_term


def display_active_filters(selected_tab, selected_tags, search_term):
    """Display chips for active filters."""
    active_filters = []
    
    if selected_tab != "All":
        active_filters.append(sac.ChipItem(label=f"Creator: {selected_tab}"))
    
    if selected_tags:
        active_filters.append(sac.ChipItem(label=f"Tags: {len(selected_tags)} selected"))
    
    if search_term:
        active_filters.append(sac.ChipItem(label="Search active"))
    
    if active_filters:
        st.markdown("**Active Filters:**")
        # Generate a unique key based on the current filters
        filter_key = f"active_filters_{hash(str(selected_tab) + str(len(selected_tags)) + search_term)}"
        sac.chip(
            items=active_filters,
            index=list(range(len(active_filters))),
            radius='md',
            color='blue',
            variant='light',
            key=filter_key
        )
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
        
        for index, project in enumerate(filtered_projects):
            create_project_card(project, index)
            st.markdown("")  # Add spacing between cards


def main():
    """Main function to display the projects page."""
    st.title("Projects")
    
    # Load CSS
    load_all_css("projects")
    
    # Initialize navigation (this will call create_navbar internally)
    initialize_navigation()
    
    # Get project filter from session state (set by navbar)
    project_filter = st.session_state.get("project_filter", "all_projects")
    
    # Determine which projects to show based on filter
    if project_filter == "github_repos":
        # Fetch GitHub repos
        github_username = SITE_CONFIG.get("github_username", "")
        if github_username:
            projects = fetch_github_repos(github_username)
        else:
            # Fallback to local data if GitHub username is not provided
            try:
                with open(Path(__file__).parent.parent / "data" / "projects.json", "r") as f:
                    projects = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                projects = []
    else:
        # Use sample projects
        projects = SAMPLE_PROJECTS
        
        # Filter based on project_filter if it's not "all_projects"
        if project_filter != "all_projects":
            filter_mapping = {
                "data_science": ["Data Science", "Pandas", "Numpy", "Data Analysis", "Visualization"],
                "web_dev": ["Web Development", "HTML", "CSS", "JavaScript", "React", "Streamlit"],
                "ml": ["Machine Learning", "Scikit-learn", "XGBoost", "TensorFlow", "PyTorch"]
            }
            
            if project_filter in filter_mapping:
                filter_tags = filter_mapping[project_filter]
                projects = [
                    p for p in projects 
                    if any(tag in p.get("tags", []) for tag in filter_tags)
                ]
    
    # Filter section with modern styling
    st.markdown("<h2>Filter Projects</h2>", unsafe_allow_html=True)
    
    with ui.card(key="filter_card"):
        # Create tabs for project categories
        category_tabs = sac.tabs(
            items=[
                sac.TabsItem(label="All", icon="grid-fill"),
                sac.TabsItem(label="Data Science", icon="bar-chart-fill"),
                sac.TabsItem(label="Web Development", icon="globe"),
                sac.TabsItem(label="Machine Learning", icon="robot"),
            ],
            align="start",
            variant="pills",
            key="category_tabs"
        )
        
        # Get all unique tags from sample projects
        all_tags = []
        for project in SAMPLE_PROJECTS:
            all_tags.extend(project.get("tags", []))
        unique_tags = sorted(list(set(all_tags)))
        
        # Create tag filter chips
        st.markdown("<h4>Filter by Technology</h4>", unsafe_allow_html=True)
        selected_tags = sac.chip(
            items=[sac.ChipItem(label=tag) for tag in unique_tags],
            index=None,
            align="start",
            size="sm",
            radius="md",
            variant="light",
            color="blue",
            multiple=True,
            key="tag_filter"
        )
        
        # Search box
        st.markdown("<h4>Search Projects</h4>", unsafe_allow_html=True)
        search_term = st.text_input("", placeholder="Search by keyword...", key="project_search")
    
    # Filter projects based on selection
    filtered_projects = projects.copy()
    
    # Apply category filter
    if category_tabs != "All":
        filter_mapping = {
            "Data Science": ["Data Science", "Pandas", "Numpy", "Data Analysis", "Visualization"],
            "Web Development": ["Web Development", "HTML", "CSS", "JavaScript", "React", "Streamlit"],
            "Machine Learning": ["Machine Learning", "Scikit-learn", "XGBoost", "TensorFlow", "PyTorch"]
        }
        
        if category_tabs in filter_mapping:
            filter_tags = filter_mapping[category_tabs]
            filtered_projects = [
                p for p in filtered_projects 
                if any(tag in p.get("tags", []) for tag in filter_tags)
            ]
    
    # Apply tag filter
    if selected_tags:
        filtered_projects = [
            p for p in filtered_projects 
            if any(tag in p.get("tags", []) for tag in selected_tags)
        ]
    
    # Apply search filter
    if search_term:
        search_term = search_term.lower()
        filtered_projects = [
            p for p in filtered_projects 
            if (search_term in p.get("title", "").lower() or 
                search_term in p.get("description", "").lower() or
                any(search_term in tag.lower() for tag in p.get("tags", [])))
        ]
    
    # Display filter summary
    if category_tabs != "All" or selected_tags or search_term:
        filter_summary = []
        if category_tabs != "All":
            filter_summary.append(f"Category: {category_tabs}")
        if selected_tags:
            filter_summary.append(f"Technologies: {', '.join(selected_tags)}")
        if search_term:
            filter_summary.append(f"Search: '{search_term}'")
        
        st.markdown(f"<div class='filter-summary'>Filtering by: {' | '.join(filter_summary)}</div>", unsafe_allow_html=True)
    
    # Display projects
    st.markdown(f"<h2>Showing {len(filtered_projects)} Projects</h2>", unsafe_allow_html=True)
    
    if filtered_projects:
        # Sort projects by title (alphabetically)
        if project_filter == "github_repos":
            # For GitHub repos, sort by stars
            filtered_projects.sort(key=lambda x: x.get('stars', 0), reverse=True)
        else:
            # For sample projects, sort by title
            filtered_projects.sort(key=lambda x: x.get('title', ''))
        
        # Display projects in cards
        for index, project in enumerate(filtered_projects):
            create_project_card(project, index)
            st.markdown("")  # Add spacing between cards
    else:
        st.info("No projects match your filter criteria. Try adjusting your filters.")
    
    # Create footer
    create_footer()


if __name__ == "__main__":
    main() 