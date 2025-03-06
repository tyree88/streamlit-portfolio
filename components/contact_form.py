"""
Contact information component for the Streamlit portfolio.
"""

import streamlit as st
from typing import Optional
import streamlit_shadcn_ui as ui
from components.social_links import create_social_links as social_links


def create_social_links(
    github_url: Optional[str] = None,
    linkedin_url: Optional[str] = None,
    bluesky_url: Optional[str] = None,
    key: str = "social_links",
    show_header: bool = True,
    show_description: bool = True
) -> None:
    """
    Display social media links with modern buttons.
    
    Args:
        github_url: GitHub profile URL
        linkedin_url: LinkedIn profile URL
        bluesky_url: Bluesky profile URL
        key: Unique key for the component
        show_header: Whether to show the header text
        show_description: Whether to show the description text
    """
    if show_header:
        ui.element("h3", children=["Connect With Me"], className="text-xl font-bold", key=f"{key}_header")
    
    if show_description:
        ui.element("p", children=["You can reach out to me through any of the following platforms:"], key=f"{key}_desc")
    
    # Use the improved social links component
    social_links(
        github_url=github_url,
        linkedin_url=linkedin_url,
        bluesky_url=bluesky_url,
        key=key,
        show_header=False
    )


def contact_info(
    github_url: Optional[str] = None,
    linkedin_url: Optional[str] = None,
    bluesky_url: Optional[str] = None,
    key: str = "contact_info",
    use_card: bool = True
) -> None:
    """
    Display contact information with social links.
    
    Args:
        github_url: GitHub profile URL
        linkedin_url: LinkedIn profile URL
        bluesky_url: Bluesky profile URL
        key: Unique key for the component
        use_card: Whether to wrap the content in a card
    """
    if use_card:
        with ui.card(key=f"{key}_card"):
            create_social_links(
                github_url=github_url,
                linkedin_url=linkedin_url,
                bluesky_url=bluesky_url,
                key=key
            )
    else:
        create_social_links(
            github_url=github_url,
            linkedin_url=linkedin_url,
            bluesky_url=bluesky_url,
            key=key
        ) 