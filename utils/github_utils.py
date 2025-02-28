"""
GitHub integration utilities.
"""

import requests
import streamlit as st
from typing import List, Dict, Any, Optional
import datetime


@st.cache_data(ttl=3600)
def fetch_github_repos(username: str, token: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Fetch GitHub repositories for a user.
    
    Args:
        username: GitHub username
        token: GitHub personal access token (optional)
        
    Returns:
        List of repository dictionaries
    """
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"
    
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        st.error(f"Error fetching GitHub repositories: {response.status_code}")
        return []
    
    repos = response.json()
    
    # Process and filter repositories
    processed_repos = []
    for repo in repos:
        # Skip forks unless they have significant contributions
        if repo.get("fork", False) and repo.get("stargazers_count", 0) < 5:
            continue
            
        # Skip empty repositories
        if not repo.get("description") and repo.get("stargazers_count", 0) == 0:
            continue
            
        # Format dates
        created_at = datetime.datetime.strptime(
            repo.get("created_at", ""), "%Y-%m-%dT%H:%M:%SZ"
        ).strftime("%b %Y") if repo.get("created_at") else ""
        
        updated_at = datetime.datetime.strptime(
            repo.get("updated_at", ""), "%Y-%m-%dT%H:%M:%SZ"
        ).strftime("%b %Y") if repo.get("updated_at") else ""
        
        # Create processed repository object
        processed_repo = {
            "name": repo.get("name", ""),
            "full_name": repo.get("full_name", ""),
            "description": repo.get("description", "No description provided"),
            "html_url": repo.get("html_url", ""),
            "stars": repo.get("stargazers_count", 0),
            "forks": repo.get("forks_count", 0),
            "language": repo.get("language", ""),
            "created_at": created_at,
            "updated_at": updated_at,
            "topics": repo.get("topics", []),
            "homepage": repo.get("homepage", "")
        }
        
        processed_repos.append(processed_repo)
    
    # Sort by stars (descending)
    processed_repos.sort(key=lambda x: x["stars"], reverse=True)
    
    return processed_repos


def get_github_contribution_chart(username: str) -> str:
    """
    Get the URL for a GitHub contribution chart image.
    
    Args:
        username: GitHub username
        
    Returns:
        URL to the contribution chart image
    """
    return f"https://ghchart.rshah.org/{username}" 