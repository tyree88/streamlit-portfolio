"""
Hero section component for the Streamlit portfolio.
"""

import streamlit as st
from typing import Optional
from config import SITE_CONFIG
from streamlit_shadcn_ui import card
from streamlit_shadcn_ui import button


def create_hero_section(
    title: Optional[str] = None,
    subtitle: Optional[str] = None,
    description: Optional[str] = None,
    primary_button_text: str = "View Projects",
    secondary_button_text: str = "Contact Me",
    key: str = "hero_section"
) -> None:
    """
    Create a hero section with title, subtitle, description, and call-to-action buttons.
    
    Args:
        title: Title to display
        subtitle: Subtitle to display
        description: Description to display
        primary_button_text: Text for the primary button
        secondary_button_text: Text for the secondary button
        key: Unique key for the component
    """
    # Use config values if not provided
    title = title or SITE_CONFIG.get("title", "Portfolio")
    subtitle = subtitle or SITE_CONFIG.get("subtitle", "Data Science & Development")
    description = description or SITE_CONFIG.get("description", "")
    
    with card(key="hero_card"):
        st.markdown(f"<h1 class='main-header'>{title}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p class='subheader'>{subtitle}</p>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(description)
        with col2:
            button(primary_button_text, variant="default", size="lg", class_name="w-full mb-2", key=f"{key}_primary_btn")
            button(secondary_button_text, variant="outline", size="lg", class_name="w-full", key=f"{key}_secondary_btn") 