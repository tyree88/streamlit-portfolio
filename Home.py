import streamlit as st
from config import SITE_CONFIG
import os

def setup_page_config():
    """Configure the Streamlit page settings."""
    st.set_page_config(
        page_title=SITE_CONFIG["title"],
        page_icon=SITE_CONFIG["icon"],
        layout="wide",
        initial_sidebar_state="expanded",
    )

def load_css():
    """Load custom CSS."""
    css_path = "assets/css/style.css"
    if os.path.exists(css_path):
        with open(css_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        # Apply default styling if CSS file doesn't exist
        st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        h1, h2, h3 {
            color: #4257b2;
        }
        </style>
        """, unsafe_allow_html=True)

def main():
    """Main function to run the Streamlit app."""
    setup_page_config()
    
    try:
        load_css()
    except FileNotFoundError:
        st.warning("Custom CSS file not found. Using default styling.")
    
    # Header section
    st.title(SITE_CONFIG["title"])
    st.subheader(SITE_CONFIG["subtitle"])
    
    # Introduction
    st.markdown("""
    Welcome to my portfolio! This is the main page of my Streamlit application.
    Use the sidebar to navigate to different sections.
    """)
    
    # Main content
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.header("About Me")
        st.markdown("""
        I'm a passionate developer with expertise in data science, 
        machine learning, and web development. This portfolio showcases 
        my projects and skills.
        """)
        
        st.button("View My Projects", use_container_width=True)
    

    
    # Featured project section
    st.header("Featured Project")
    with st.container():
        st.subheader("Project Title")
        st.markdown("""
        Brief description of your featured project. Highlight the key 
        technologies used and the problem it solves.
        """)
        
        st.progress(100)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Technology", "Python")
        col2.metric("Category", "Data Science")
        col3.metric("Completion", "100%")

if __name__ == "__main__":
    main() 