"""
Navigation bar component for the Streamlit portfolio.
"""

import streamlit as st
from typing import List, Dict, Any, Optional
from streamlit_option_menu import option_menu


def create_navbar(
    menu_items: List[Dict[str, Any]],
    default_index: int = 0,
    orientation: str = "horizontal",
    key: Optional[str] = None
) -> str:
    """
    Create a navigation bar using streamlit-option-menu.
    
    Args:
        menu_items: List of menu items with 'name' and 'icon' keys
        default_index: Default selected index
        orientation: 'horizontal' or 'vertical'
        key: Optional key for the component
        
    Returns:
        Selected menu item name
    """
    icons = [item.get("icon", "house") for item in menu_items]
    labels = [item.get("name", f"Item {i+1}") for i, item in enumerate(menu_items)]
    
    if orientation == "horizontal":
        selected = option_menu(
            menu_title=None,
            options=labels,
            icons=icons,
            default_index=default_index,
            orientation="horizontal",
            styles={
                "container": {"padding": "0px", "background-color": "transparent"},
                "icon": {"color": "#4257b2", "font-size": "16px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "center",
                    "margin": "0px",
                    "padding": "10px",
                    "--hover-color": "#f0f2f6",
                },
                "nav-link-selected": {"background-color": "#4257b2", "color": "white"},
            },
            key=key or "horizontal_navbar"
        )
    else:
        selected = option_menu(
            menu_title="Navigation",
            options=labels,
            icons=icons,
            default_index=default_index,
            styles={
                "container": {"padding": "0px", "background-color": "#f0f2f6"},
                "icon": {"color": "#4257b2", "font-size": "16px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "padding": "10px",
                },
                "nav-link-selected": {"background-color": "#4257b2", "color": "white"},
            },
            key=key or "vertical_navbar"
        )
    
    return selected 