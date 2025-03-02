"""
Profile card component for the Streamlit portfolio.
"""

import streamlit as st
from typing import Optional
from config import SITE_CONFIG
from streamlit_shadcn_ui import card
from streamlit_shadcn_ui import avatar
from streamlit_shadcn_ui import button
from streamlit_shadcn_ui.py_components.badges import badges


def create_profile_card(
    name: Optional[str] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    image: Optional[str] = None,
    show_buttons: bool = True,
    key: str = "profile_card"
) -> None:
    """
    Create a profile card with image, name, title, and description.
    
    Args:
        name: Name to display
        title: Title/subtitle to display
        description: Description to display
        image: URL or path to profile image
        show_buttons: Whether to show social buttons
        key: Unique key for the component
    """
    # Use config values if not provided
    name = name or SITE_CONFIG.get("author", SITE_CONFIG.get("name", ""))
    title = title or SITE_CONFIG.get("subtitle", SITE_CONFIG.get("tagline", ""))
    description = description or SITE_CONFIG.get("description", "")
    image = image or SITE_CONFIG.get("profile_pic", "https://via.placeholder.com/150")
    
    with card(key=key):
        col1, col2 = st.columns([1, 3])
        
        with col1:
            # Use avatar component instead of image
            avatar(
                image,
                size="xl",
                key=f"{key}_avatar"
            )
        
        with col2:
            st.markdown(f"# {name}")
            st.markdown(f"## {title}")
            st.markdown(description)
            
            # Contact buttons
            if show_buttons:
                col_btn1, col_btn2, _ = st.columns([1, 1, 2])
                
                with col_btn1:
                    if "github" in SITE_CONFIG and SITE_CONFIG["github"]:
                        button("GitHub", variant="default", size="sm", key=f"{key}_github_btn")
                
                with col_btn2:
                    if "linkedin" in SITE_CONFIG and SITE_CONFIG["linkedin"]:
                        button("LinkedIn", variant="outline", size="sm", key=f"{key}_linkedin_btn")