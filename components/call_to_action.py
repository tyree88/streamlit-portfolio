"""
Call-to-action component for the Streamlit portfolio.
"""

import streamlit as st
from typing import Optional
from streamlit_shadcn_ui.card import card
from streamlit_shadcn_ui.button import button


def create_call_to_action(
    title: str = "Let's Work Together",
    message: Optional[str] = None,
    button_text: str = "Contact Me",
    button_key: str = "cta_btn",
    use_card: bool = True,
    class_name: str = "mb-4"
) -> None:
    """
    Create a call-to-action section with a title, message, and button.
    
    Args:
        title: Title of the call-to-action
        message: Message to display
        button_text: Text for the button
        button_key: Key for the button
        use_card: Whether to use a card for the call-to-action
        class_name: Additional CSS class names
    """
    # Default message if not provided
    if not message:
        message = (
            "I'm always open to new opportunities and collaborations. "
            "Feel free to reach out if you'd like to discuss a project or just connect!"
        )
    
    st.markdown(f"<h2 class='section-header'>{title}</h2>", unsafe_allow_html=True)
    
    if use_card:
        with card(key="cta_card", bordered=True, class_name=class_name):
            _create_cta_content(message, button_text, button_key)
    else:
        _create_cta_content(message, button_text, button_key)


def _create_cta_content(
    message: str,
    button_text: str,
    button_key: str
) -> None:
    """
    Create the content for the call-to-action.
    
    Args:
        message: Message to display
        button_text: Text for the button
        button_key: Key for the button
    """
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(message)
    with col2:
        button(
            button_text, 
            variant="default", 
            size="lg", 
            class_name="w-full", 
            key=button_key
        ) 