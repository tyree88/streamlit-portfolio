"""
Call to action component for the Streamlit portfolio.
"""

import streamlit as st
from typing import Optional
from streamlit_shadcn_ui import card
from streamlit_shadcn_ui import button


def create_call_to_action(
    title: str = "Let's Connect",
    message: Optional[str] = None,
    button_text: str = "View About",
    button_variant: str = "default",
    button_size: str = "lg",
    key: str = "cta"
) -> None:
    """
    Create a call to action section with a message and button.
    
    Args:
        title: Title of the call to action
        message: Message to display
        button_text: Text for the button
        button_variant: Variant of the button
        button_size: Size of the button
        key: Unique key for the component
    """
    # Default message if not provided
    if message is None:
        message = """
        I'm always open to new opportunities and collaborations. 
        Feel free to connect with me on social media to discuss projects or just to network!
        """
    
    # Display title
    st.markdown(f"<h2 class='section-header'>{title}</h2>", unsafe_allow_html=True)
    
    with card(key="cta_card"):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(message)
        with col2:
            button(
                button_text, 
                variant=button_variant, 
                size=button_size, 
                class_name="w-full", 
                key=f"{key}_btn"
            ) 