"""
Theme setup component for the Streamlit portfolio.
"""

import streamlit as st
import os
from typing import Optional


def load_css(custom_css_path: Optional[str] = "assets/css/style.css") -> None:
    """
    Load custom CSS from a file or use default styling.
    
    Args:
        custom_css_path: Path to the custom CSS file
    """
    if custom_css_path and os.path.exists(custom_css_path):
        with open(custom_css_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    else:
        # Default styling if CSS file doesn't exist
        st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }
        .subheader {
            font-size: 1.5rem;
            color: #4257b2;
            margin-bottom: 2rem;
        }
        .section-header {
            font-size: 1.8rem;
            margin-top: 2rem;
            margin-bottom: 1rem;
            color: #333;
        }
        .highlight {
            background-color: #f0f2f6;
            padding: 1.5rem;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
        }
        .shadcn-card {
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .shadcn-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        }
        </style>
        """, unsafe_allow_html=True)


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