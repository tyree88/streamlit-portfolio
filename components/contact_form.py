"""
Contact information component for the Streamlit portfolio.
"""

import streamlit as st
from typing import Optional
from streamlit_shadcn_ui import card


def create_social_links(
    github_url: Optional[str] = None,
    linkedin_url: Optional[str] = None,
    bluesky_url: Optional[str] = None,
    key: str = "social_links",
    columns: int = 3,
    show_header: bool = True,
    show_description: bool = True
) -> None:
    """
    Display social media links with image-based buttons.
    
    Args:
        github_url: GitHub profile URL
        linkedin_url: LinkedIn profile URL
        bluesky_url: Bluesky profile URL
        key: Unique key for the component
        columns: Number of columns for the social links
        show_header: Whether to show the header text
        show_description: Whether to show the description text
    """
    if show_header:
        st.markdown("### Connect With Me")
    
    if show_description:
        st.markdown(
            "You can reach out to me through any of the following platforms:"
        )
    
    # Social links
    social_cols = st.columns(columns)
    
    if github_url:
        social_cols[0].markdown(
            f"[![GitHub](<https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white>)]({github_url})"
        )
    
    if linkedin_url:
        social_cols[1].markdown(
            f"[![LinkedIn](<https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white>)]({linkedin_url})"
        )
    
    if bluesky_url:
        social_cols[2].markdown(
            f"[![🦋 Bluesky](<https://img.shields.io/badge/Bluesky-0285FF?style=for-the-badge&logo=bluesky&logoColor=white>)]({bluesky_url})"
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
        with card(key=f"{key}_card"):
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