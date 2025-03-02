"""
Skill card component for the Streamlit portfolio.
"""

import streamlit as st
from typing import Dict, Any, List, Optional
from streamlit_shadcn_ui import card
from streamlit_shadcn_ui.py_components.badges import badges


def create_skill_card(
    title: str,
    description: str,
    skills: List[str],
    key: str
) -> None:
    """
    Create a card for displaying a skill category.
    
    Args:
        title: Title of the skill category
        description: Description of the skill category
        skills: List of skills to display as badges
        key: Unique key for the component
    """
    with card(key=key):
        st.markdown(f"### {title}")
        st.markdown(description)
        
        badge_list = [(skill, "outline") for skill in skills]
        badges(badge_list, key=f"{key}_skills")


def create_skills_section(
    skills_data: List[Dict[str, Any]],
    columns: int = 3
) -> None:
    """
    Create a section with multiple skill cards.
    
    Args:
        skills_data: List of skill category dictionaries
        columns: Number of columns to display skills in
    """
    # Create columns
    cols = st.columns(columns)
    
    # Add skill cards to columns
    for i, skill in enumerate(skills_data):
        with cols[i % columns]:
            create_skill_card(
                title=skill.get("title", f"Skill Category {i+1}"),
                description=skill.get("description", ""),
                skills=skill.get("skills", []),
                key=f"skill_{i}"
            ) 