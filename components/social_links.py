"""
Social links component for the Streamlit portfolio.
"""

import streamlit as st
from typing import Dict, List, Tuple
from config import SITE_CONFIG
from streamlit_shadcn_ui import button
from streamlit_shadcn_ui.py_components.badges import badges


def create_social_badges(class_name: str = "flex flex-wrap gap-2") -> None:
    """
    Create social media badges.
    
    Args:
        class_name: Additional CSS class names
    """
    social_links = []
    
    if "github" in SITE_CONFIG and SITE_CONFIG["github"]:
        social_links.append(("GitHub", "default"))
    
    if "linkedin" in SITE_CONFIG and SITE_CONFIG["linkedin"]:
        social_links.append(("LinkedIn", "secondary"))
    
    if "bluesky" in SITE_CONFIG and SITE_CONFIG["bluesky"]:
        social_links.append(("🦋 Bluesky", "destructive"))
    
    if social_links:
        badges(social_links, class_name=class_name, key="social_badges")


def create_social_links(github_url: str = None, linkedin_url: str = None, bluesky_url: str = None, 
                        key: str = "social", show_header: bool = True) -> None:
    """
    Create social media links section.
    
    Args:
        github_url: GitHub profile URL
        linkedin_url: LinkedIn profile URL
        bluesky_url: Bluesky profile URL
        key: Unique key for the component
        show_header: Whether to show the section header
    """
    if show_header:
        st.markdown("### Connect With Me")
    
    social_cols = st.columns(3)
    
    col_idx = 0
    
    if github_url:
        with social_cols[col_idx % 3]:
            if button("GitHub", variant="default", size="sm", key=f"github_btn_{key}"):
                st.markdown(f'<script>window.open("{github_url}", "_blank");</script>', unsafe_allow_html=True)
        col_idx += 1
    
    if linkedin_url:
        with social_cols[col_idx % 3]:
            if button("LinkedIn", variant="secondary", size="sm", key=f"linkedin_btn_{key}"):
                st.markdown(f'<script>window.open("{linkedin_url}", "_blank");</script>', unsafe_allow_html=True)
        col_idx += 1
    
    if bluesky_url:
        with social_cols[col_idx % 3]:
            if button("Bluesky", variant="outline", size="sm", key=f"bluesky_btn_{key}"):
                st.markdown(f'<script>window.open("{bluesky_url}", "_blank");</script>', unsafe_allow_html=True)
        col_idx += 1 