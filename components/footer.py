"""
Footer component for the Streamlit portfolio.
"""

import streamlit as st
from config import SITE_CONFIG


def create_footer():
    """
    Create a footer with social links and copyright information.
    """
    st.markdown("---")
    
    cols = st.columns([1, 1, 1])
    
    # GitHub link
    if "github" in SITE_CONFIG and SITE_CONFIG["github"]:
        cols[0].markdown(
            f'<a href="{SITE_CONFIG["github"]}" target="_blank">'
            f'<i class="fab fa-github" style="font-size: 1.5rem; color: #333;"></i></a>',
            unsafe_allow_html=True
        )
    
    # LinkedIn link
    if "linkedin" in SITE_CONFIG and SITE_CONFIG["linkedin"]:
        cols[1].markdown(
            f'<a href="{SITE_CONFIG["linkedin"]}" target="_blank">'
            f'<i class="fab fa-linkedin" style="font-size: 1.5rem; color: #0077b5;"></i></a>',
            unsafe_allow_html=True
        )
    
    # Bluesky link
    if "bluesky" in SITE_CONFIG and SITE_CONFIG.get("bluesky"):
        cols[2].markdown(
            f'<a href="{SITE_CONFIG["bluesky"]}" target="_blank">'
            f'<span style="font-size: 1.5rem; color: #0285FF;">🦋</span></a>',
            unsafe_allow_html=True
        )
    
    # Copyright information
    current_year = st.session_state.get("current_year", 2023)
    st.markdown(
        f'<div style="text-align: center; margin-top: 1rem; color: #6c757d; font-size: 0.8rem;">'
        f'© {current_year} {SITE_CONFIG.get("author", "Your Name")}. All rights reserved.'
        f'</div>',
        unsafe_allow_html=True
    )
    
    # Add Font Awesome for icons
    st.markdown(
        """
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        """,
        unsafe_allow_html=True
    ) 