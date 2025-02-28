"""
GitHub repository card component for the Streamlit portfolio.
"""

import streamlit as st
from typing import Dict, Any, List
from streamlit_shadcn_ui import card
from streamlit_shadcn_ui import button


def create_repo_card(
    repo: Dict[str, Any],
    key_prefix: str = "repo",
    class_name: str = "mb-3"
) -> None:
    """
    Create a card for displaying a GitHub repository.
    
    Args:
        repo: Dictionary with repository details
        key_prefix: Prefix for the component keys
        class_name: Additional CSS class names
    """
    with card(key=f"{key_prefix}_{repo['name']}", bordered=True, class_name=class_name):
        st.markdown(f"### {repo['name']}")
        st.markdown(repo.get("description") or "No description available")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Stars", repo.get("stars", 0))
        col2.metric("Forks", repo.get("forks", 0))
        col3.metric("Language", repo.get("language") or "N/A")
        
        button(
            "View Repository", 
            variant="default", 
            size="sm", 
            key=f"view_{key_prefix}_{repo['name']}"
        )


def create_github_repos_section(
    repos: List[Dict[str, Any]],
    max_repos: int = 5,
    show_view_all: bool = True,
    github_url: str = None
) -> None:
    """
    Create a section displaying GitHub repositories.
    
    Args:
        repos: List of repository dictionaries
        max_repos: Maximum number of repositories to display
        show_view_all: Whether to show a link to view all repositories
        github_url: URL to the GitHub profile
    """
    st.header("GitHub Repositories")
    
    if not repos:
        st.info("No GitHub repositories found.")
        return
    
    # Display repositories
    for repo in repos[:max_repos]:
        create_repo_card(repo)
    
    # Show link to view all repositories
    if show_view_all and github_url:
        st.markdown(f"[View all repositories]({github_url})") 