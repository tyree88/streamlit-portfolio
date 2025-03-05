"""
GitHub repository card component for the Streamlit portfolio.
"""

import streamlit as st
from typing import Dict, Any, List
from streamlit_shadcn_ui import card
from streamlit_shadcn_ui import button
from streamlit_shadcn_ui import badges


def create_repo_card(
    repo: Dict[str, Any],
    key_prefix: str = "repo"
) -> None:
    """
    Create a card for displaying a GitHub repository.
    
    Args:
        repo: Dictionary with repository details
        key_prefix: Prefix for the component keys
    """
    with card(key=f"{key_prefix}_{repo['name']}"):
        # Repository name with custom styling
        st.markdown(f"<div class='repo-name'>{repo['name']}</div>", unsafe_allow_html=True)
        
        # Repository description
        description = repo.get("description") or "No description available"
        st.markdown(f"<div class='repo-description'>{description}</div>", unsafe_allow_html=True)
        
        # Repository metrics using badges
        badge_items = []
        
        # Stars
        badge_items.append((f"⭐ {repo.get('stars', 0)}", "default"))
        
        # Forks
        badge_items.append((f"🔄 {repo.get('forks', 0)}", "outline"))
        
        # Language with color dot if available
        language = repo.get("language", "N/A")
        badge_items.append((f"📝 {language}", "secondary"))
        
        # Display badges
        badges(badge_items, key=f"metrics_{key_prefix}_{repo['name']}")
        
        # Topics if available
        if repo.get("topics"):
            st.markdown("**Topics:**")
            topic_badges = [(topic, "outline") for topic in repo.get("topics", [])[:5]]
            badges(topic_badges, key=f"topics_{key_prefix}_{repo['name']}")
        
        # View repository button
        st.markdown("")  # Add spacing
        button(
            "View Repository", 
            variant="default", 
            size="sm", 
            key=f"view_{key_prefix}_{repo['name']}"
        )


def create_repos_section(
    repos: List[Dict[str, Any]],
    max_repos: int = 5,
    key_prefix: str = "repo"
) -> None:
    """
    Create a section with GitHub repository cards.
    
    Args:
        repos: List of repository dictionaries
        max_repos: Maximum number of repositories to display
        key_prefix: Prefix for the component keys
    """
    for i, repo in enumerate(repos[:max_repos]):
        create_repo_card(repo, key_prefix=f"{key_prefix}_{i}")
        st.markdown("")  # Add some spacing between cards


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
    if not repos:
        st.info("No GitHub repositories found.")
        return
    
    # Filter options
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_term = st.text_input("Search repositories", key="repo_search")
    
    with col2:
        sort_option = st.selectbox(
            "Sort by", 
            ["Stars", "Recently Updated", "Name"],
            key="repo_sort"
        )
    
    # Sort repositories based on selection
    if sort_option == "Stars":
        repos = sorted(repos, key=lambda x: x.get("stars", 0), reverse=True)
    elif sort_option == "Recently Updated":
        repos = sorted(repos, key=lambda x: x.get("updated_at", ""), reverse=True)
    elif sort_option == "Name":
        repos = sorted(repos, key=lambda x: x.get("name", "").lower())
    
    # Filter repositories based on search term
    if search_term:
        filtered_repos = []
        for repo in repos:
            name = repo.get("name", "").lower()
            description = repo.get("description", "").lower()
            language = repo.get("language", "").lower()
            topics = [t.lower() for t in repo.get("topics", [])]
            
            search_term_lower = search_term.lower()
            
            if (search_term_lower in name or 
                search_term_lower in description or 
                search_term_lower in language or
                any(search_term_lower in topic for topic in topics)):
                filtered_repos.append(repo)
        repos = filtered_repos
    
    # Display repositories
    if repos:
        st.markdown(f"Showing {min(len(repos), max_repos)} of {len(repos)} repositories")
        create_repos_section(repos, max_repos)
        
        # Show link to view all repositories
        if show_view_all and github_url and len(repos) > max_repos:
            st.markdown("")
            button(
                "View All Repositories on GitHub", 
                variant="outline", 
                size="sm", 
                key="view_all_repos"
            )
    else:
        st.info("No repositories match your search criteria.") 