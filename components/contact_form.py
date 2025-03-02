"""
Contact information component for the Streamlit portfolio.
"""

import streamlit as st
from typing import Optional
from streamlit_shadcn_ui import card
from streamlit_shadcn_ui import button
from streamlit_shadcn_ui.py_components.badges import badges


def contact_info(
    github_url: Optional[str] = None,
    linkedin_url: Optional[str] = None,
    bluesky_url: Optional[str] = None,
    key: str = "contact_info"
) -> None:
    """
    Display contact information and social links.
    
    Args:
        github_url: GitHub profile URL
        linkedin_url: LinkedIn profile URL
        bluesky_url: Bluesky profile URL
        key: Unique key for the component
    """
    st.markdown("### Connect With Me")
    st.markdown(
        "You can reach out to me through any of the following platforms:"
    )
    
    # Social links
    st.markdown("### Social Profiles")
    
    # Display social badges
    badge_list = []
    
    if github_url:
        badge_list.append(("GitHub", "outline"))
    
    if linkedin_url:
        badge_list.append(("LinkedIn", "outline"))
    
    if bluesky_url:
        badge_list.append(("🦋 Bluesky", "outline"))
    
    if badge_list:
        badges(badge_list, key=f"{key}_social_badges")
    
    # Social buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if github_url:
            button(
                "GitHub Profile", 
                variant="default", 
                size="sm", 
                key=f"{key}_github_btn",
                class_name="w-full"
            )
    
    with col2:
        if linkedin_url:
            button(
                "LinkedIn Profile", 
                variant="outline", 
                size="sm", 
                key=f"{key}_linkedin_btn",
                class_name="w-full"
            )
    
    with col3:
        if bluesky_url:
            button(
                "Bluesky Profile", 
                variant="secondary", 
                size="sm", 
                key=f"{key}_bluesky_btn",
                class_name="w-full"
            ) 