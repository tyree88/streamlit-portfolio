"""
Page header component for the Streamlit portfolio.
"""

import streamlit as st
from typing import Optional
from config import SITE_CONFIG


def setup_page(
    page_title: Optional[str] = None,
    page_icon: Optional[str] = None,
    layout: str = "wide",
    initial_sidebar_state: str = "expanded"
) -> None:
    """
    Set up the page configuration.
    
    Args:
        page_title: Title of the page
        page_icon: Icon for the page
        layout: Layout of the page
        initial_sidebar_state: Initial state of the sidebar
    """
    # Determine page title
    if page_title:
        full_title = f"{page_title} | {SITE_CONFIG['title']}"
    else:
        full_title = SITE_CONFIG['title']
    
    # Page configuration
    st.set_page_config(
        page_title=full_title,
        page_icon=page_icon or SITE_CONFIG.get("icon"),
        layout=layout,
        initial_sidebar_state=initial_sidebar_state,
    )


def create_page_header(
    title: str,
    subtitle: Optional[str] = None,
    use_container: bool = False
) -> None:
    """
    Create a page header with title and optional subtitle.
    
    Args:
        title: Title of the page
        subtitle: Subtitle of the page
        use_container: Whether to use a container for the header
    """
    if use_container:
        with st.container():
            st.title(title)
            if subtitle:
                st.markdown(subtitle)
    else:
        st.title(title)
        if subtitle:
            st.markdown(subtitle)


def create_sidebar_profile() -> None:
    """
    Create a sidebar profile with image, name, and tagline.
    """
    st.sidebar.image(
        SITE_CONFIG.get("profile_pic", "https://via.placeholder.com/150"),
        width=150,
    )
    st.sidebar.title(SITE_CONFIG.get("name", SITE_CONFIG.get("author", "Portfolio")))
    st.sidebar.markdown(SITE_CONFIG["tagline"]) 