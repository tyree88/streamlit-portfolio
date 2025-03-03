"""
Navigation component for the Streamlit portfolio.
"""

import streamlit as st
from streamlit_shadcn_ui import button
from streamlit_shadcn_ui import card


def create_navbar(current_page: str = "home") -> None:
    """
    Create a navigation bar with modern styling.
    
    Args:
        current_page: The current active page
    """
    with card(key="navbar_card"):
        cols = st.columns([1, 2, 1])
        
        with cols[1]:
            nav_cols = st.columns(4)
            
            # Home button
            with nav_cols[0]:
                if button(
                    "Home",
                    variant="ghost" if current_page != "home" else "default",
                    size="sm",
                    class_name="w-full",
                    key="nav_home"
                ):
                    st.switch_page("Home.py")
            
            # About button
            with nav_cols[1]:
                if button(
                    "About",
                    variant="ghost" if current_page != "about" else "default",
                    size="sm",
                    class_name="w-full",
                    key="nav_about"
                ):
                    st.switch_page("pages/About.py")
            
            # Projects button
            with nav_cols[2]:
                if button(
                    "Projects",
                    variant="ghost" if current_page != "projects" else "default",
                    size="sm",
                    class_name="w-full",
                    key="nav_projects"
                ):
                    st.switch_page("pages/Projects.py")
            
            # Blog button
            with nav_cols[3]:
                if button(
                    "Blog",
                    variant="ghost" if current_page != "blog" else "default",
                    size="sm",
                    class_name="w-full",
                    key="nav_blog"
                ):
                    st.switch_page("pages/Blog.py") 