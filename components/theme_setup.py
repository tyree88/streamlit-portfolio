"""
Theme setup component for the Streamlit portfolio.
"""

import streamlit as st
import os
from typing import Optional
from utils.display_utils import load_css_file


def load_css(custom_css_path: Optional[str] = None) -> None:
    """
    Load CSS files for the application.
    
    Args:
        custom_css_path: Optional path to a custom CSS file
    """
    # Load common CSS
    load_css_file("assets/css/pages/common.css")
    
    # Load custom CSS if provided
    if custom_css_path and os.path.exists(custom_css_path):
        load_css_file(custom_css_path)


def add_custom_fonts() -> None:
    """
    Add custom fonts to the application.
    """
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)


def add_font_awesome() -> None:
    """
    Add Font Awesome icons to the application.
    """
    st.markdown(
        """
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        """,
        unsafe_allow_html=True
    ) 