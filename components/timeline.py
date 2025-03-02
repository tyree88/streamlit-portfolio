"""
Timeline component for the Streamlit portfolio.
"""

import streamlit as st
from typing import List, Dict, Any
from streamlit_shadcn_ui import card
from streamlit_shadcn_ui.py_components.badges import badges


def create_timeline_item(
    title: str,
    period: str,
    organization: str,
    description: str,
    show_divider: bool = True
) -> None:
    """
    Create a timeline item with title, period, organization, and description.
    
    Args:
        title: Title of the timeline item
        period: Period of the timeline item
        organization: Organization of the timeline item
        description: Description of the timeline item
        show_divider: Whether to show a divider after the item
    """
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.markdown(f"**{period}**")
        badges([(organization, "outline")], key=f"org_{title.lower().replace(' ', '_')}")
    
    with col2:
        st.markdown(f"### {title}")
        st.markdown(description)
    
    if show_divider:
        st.markdown("---")


def create_timeline(
    items: List[Dict[str, Any]],
    title_key: str = "title",
    period_key: str = "period",
    organization_key: str = "company",
    description_key: str = "description",
    key: str = "timeline_card"
) -> None:
    """
    Create a timeline of items (experience, education, etc.) in a card.
    
    Args:
        items: List of dictionaries with timeline items
        title_key: Key for the title in the item dictionary
        period_key: Key for the period in the item dictionary
        organization_key: Key for the organization in the item dictionary
        description_key: Key for the description in the item dictionary
        key: Unique key for the component
    """
    with card(key=key):
        for i, item in enumerate(items):
            create_timeline_item(
                title=item.get(title_key, ""),
                period=item.get(period_key, ""),
                organization=item.get(organization_key, ""),
                description=item.get(description_key, ""),
                show_divider=(i < len(items) - 1)  # Don't show divider for last item
            )


def create_experience_section(
    experience_items: List[Dict[str, Any]],
    key: str = "experience_timeline"
) -> None:
    """
    Create an experience timeline section.
    
    Args:
        experience_items: List of dictionaries with experience items
        key: Unique key for the component
    """
    create_timeline(
        items=experience_items,
        title_key="title",
        period_key="period",
        organization_key="company",
        description_key="description",
        key=key
    )


def create_education_section(
    education_items: List[Dict[str, Any]],
    key: str = "education_timeline"
) -> None:
    """
    Create an education timeline section.
    
    Args:
        education_items: List of dictionaries with education items
        key: Unique key for the component
    """
    create_timeline(
        items=education_items,
        title_key="title",
        period_key="period",
        organization_key="institution",
        description_key="description",
        key=key
    ) 