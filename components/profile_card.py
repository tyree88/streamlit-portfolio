"""
Profile card component for the Streamlit portfolio.
"""

import streamlit as st
from typing import Optional
from streamlit_shadcn_ui import card
from streamlit_shadcn_ui import button
from streamlit_shadcn_ui import avatar
from config import SITE_CONFIG


def create_profile_card(
    name: Optional[str] = None,
    title: Optional[str] = None,
    bio: Optional[str] = None,
    profile_pic: Optional[str] = None,
    show_buttons: bool = True,
    key: str = "profile_card",
    class_name: str = "mb-4"
) -> None:
    """
    Create a profile card with avatar, name, title, bio, and social buttons.
    
    Args:
        name: Name to display
        title: Title/subtitle to display
        bio: Biography text
        profile_pic: URL to profile picture
        show_buttons: Whether to show social buttons
        key: Unique key for the component
        class_name: Additional CSS class names
    """
    # Use config values if not provided
    name = name or SITE_CONFIG.get("author", SITE_CONFIG.get("name", "Your Name"))
    title = title or SITE_CONFIG.get("subtitle", "Data Scientist & Developer")
    profile_pic = profile_pic or SITE_CONFIG.get("profile_pic", "https://via.placeholder.com/150")
    
    # Default bio if not provided
    if not bio:
        bio = """
        Welcome to my portfolio! I'm a passionate data scientist and developer with expertise
        in machine learning, data analysis, and web development. I love solving complex problems
        and building innovative solutions.
        
        I have experience working with Python, SQL, machine learning frameworks, and web technologies.
        My goal is to leverage data to create meaningful insights and impactful applications.
        """
    
    with card(key=key, bordered=True, class_name=class_name):
        col1, col2 = st.columns([1, 3])
        
        with col1:
            # Use avatar component
            avatar(
                profile_pic,
                size="xl",
                key=f"{key}_avatar"
            )
        
        with col2:
            st.markdown(f"# {name}")
            st.markdown(f"## {title}")
            st.markdown(bio)
            
            # Contact buttons
            if show_buttons:
                col_btn1, col_btn2, _ = st.columns([1, 1, 2])
                with col_btn1:
                    button("GitHub", variant="default", size="sm", key=f"{key}_github_btn")
                with col_btn2:
                    button("LinkedIn", variant="outline", size="sm", key=f"{key}_linkedin_btn")