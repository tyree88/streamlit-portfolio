"""
Hero section component for the Streamlit portfolio.
"""

import streamlit as st
from typing import Optional
from streamlit_shadcn_ui import card
from streamlit_shadcn_ui import button
from config import SITE_CONFIG


def create_hero_section(
    title: Optional[str] = None,
    subtitle: Optional[str] = None,
    description: Optional[str] = None,
    primary_button_text: str = "View Projects",
    secondary_button_text: str = "Contact Me",
    primary_button_key: str = "hero_primary_btn",
    secondary_button_key: str = "hero_secondary_btn",
    use_card: bool = True,
    class_name: str = "mb-4"
) -> None:
    """
    Create a hero section with title, subtitle, description, and call-to-action buttons.
    
    Args:
        title: Title of the hero section
        subtitle: Subtitle of the hero section
        description: Description of the hero section
        primary_button_text: Text for the primary button
        secondary_button_text: Text for the secondary button
        primary_button_key: Key for the primary button
        secondary_button_key: Key for the secondary button
        use_card: Whether to use a card for the hero section
        class_name: Additional CSS class names
    """
    # Use config values if not provided
    title = title or SITE_CONFIG.get("title", "Portfolio")
    subtitle = subtitle or SITE_CONFIG.get("subtitle", "Data Scientist & Developer")
    description = description or SITE_CONFIG.get("description", "")
    
    if use_card:
        with card(key="hero_card", bordered=True, class_name=class_name):
            _create_hero_content(
                title, 
                subtitle, 
                description, 
                primary_button_text, 
                secondary_button_text,
                primary_button_key,
                secondary_button_key
            )
    else:
        _create_hero_content(
            title, 
            subtitle, 
            description, 
            primary_button_text, 
            secondary_button_text,
            primary_button_key,
            secondary_button_key
        )


def _create_hero_content(
    title: str,
    subtitle: str,
    description: str,
    primary_button_text: str,
    secondary_button_text: str,
    primary_button_key: str,
    secondary_button_key: str
) -> None:
    """
    Create the content for the hero section.
    
    Args:
        title: Title of the hero section
        subtitle: Subtitle of the hero section
        description: Description of the hero section
        primary_button_text: Text for the primary button
        secondary_button_text: Text for the secondary button
        primary_button_key: Key for the primary button
        secondary_button_key: Key for the secondary button
    """
    st.markdown(f"<h1 class='main-header'>{title}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='subheader'>{subtitle}</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(description)
    with col2:
        button(
            primary_button_text, 
            variant="default", 
            size="lg", 
            class_name="w-full mb-2", 
            key=primary_button_key
        )
        button(
            secondary_button_text, 
            variant="outline", 
            size="lg", 
            class_name="w-full", 
            key=secondary_button_key
        ) 