"""
Social links component for the Streamlit portfolio.
"""

import streamlit as st
from typing import Dict, List, Tuple
from config import SITE_CONFIG
from streamlit_shadcn_ui import button
from streamlit_shadcn_ui.py_components.badges import badges


def create_social_badges(class_name: str = "") -> None:
    """
    Create social media badges.
    
    Args:
        class_name: Additional CSS class names
    """
    social_links = []
    
    if "github" in SITE_CONFIG and SITE_CONFIG["github"]:
        social_links.append(("GitHub", "outline"))
    
    if "linkedin" in SITE_CONFIG and SITE_CONFIG["linkedin"]:
        social_links.append(("LinkedIn", "outline"))
    
    if "bluesky" in SITE_CONFIG and SITE_CONFIG["bluesky"]:
        social_links.append(("🦋 Bluesky", "outline"))
    
    if social_links:
        badges(social_links, key="social_badges")


def create_social_buttons(columns: int = 3, size: str = "sm", class_name: str = "") -> None:
    """
    Create social media buttons.
    
    Args:
        columns: Number of columns to display buttons in
        size: Size of the buttons
        class_name: Additional CSS class names
    """
    social_cols = st.columns(columns)
    
    col_idx = 0
    
    if "github" in SITE_CONFIG and SITE_CONFIG["github"]:
        with social_cols[col_idx % columns]:
            button("GitHub", variant="default", size=size, key="github_btn", class_name=class_name)
        col_idx += 1
    
    if "linkedin" in SITE_CONFIG and SITE_CONFIG["linkedin"]:
        with social_cols[col_idx % columns]:
            button("LinkedIn", variant="outline", size=size, key="linkedin_btn", class_name=class_name)
        col_idx += 1
    
    if "bluesky" in SITE_CONFIG and SITE_CONFIG["bluesky"]:
        with social_cols[col_idx % columns]:
            button("Bluesky", variant="outline", size=size, key="bluesky_btn", class_name=class_name)
        col_idx += 1 