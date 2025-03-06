"""
Navigation component for the Streamlit portfolio.
"""

import streamlit as st
from streamlit_shadcn_ui import button, badges
import streamlit_antd_components as sac
from config import SITE_CONFIG
import sys


def create_navbar(current_page: str = "home") -> None:
    """
    Create a modern navigation bar with dropdown menus and integrate with Streamlit's sidebar.
    
    Args:
        current_page: The current page being displayed
    """
    # Configure the sidebar
    with st.sidebar:
        
        st.markdown("<h3>Project Categories</h3>", unsafe_allow_html=True)
        
        # Create direct buttons for project filters with unique keys based on current page
        key_prefix = f"{current_page}_"
        
        if st.button("All Projects", use_container_width=True, key=f"{key_prefix}sidebar_all_projects"):
            st.session_state.project_filter = 'all_projects'
            if current_page != 'projects':
                st.switch_page("pages/Projects.py")
            else:
                st.rerun()
                
        if st.button("Data Science", use_container_width=True, key=f"{key_prefix}sidebar_data_science"):
            st.session_state.project_filter = 'data_science'
            if current_page != 'projects':
                st.switch_page("pages/Projects.py")
            else:
                st.rerun()
                
        if st.button("Web Development", use_container_width=True, key=f"{key_prefix}sidebar_web_dev"):
            st.session_state.project_filter = 'web_dev'
            if current_page != 'projects':
                st.switch_page("pages/Projects.py")
            else:
                st.rerun()
                
        if st.button("Machine Learning", use_container_width=True, key=f"{key_prefix}sidebar_ml"):
            st.session_state.project_filter = 'ml'
            if current_page != 'projects':
                st.switch_page("pages/Projects.py")
            else:
                st.rerun()
                
        if st.button("GitHub Repos", use_container_width=True, key=f"{key_prefix}sidebar_github_repos"):
            st.session_state.project_filter = 'github_repos'
            if current_page != 'projects':
                st.switch_page("pages/Projects.py")
            else:
                st.rerun()
    
# Main navbar for desktop view
def create_desktop_navbar(current_page: str) -> None:
    """
    Create the desktop navigation bar component.
    
    Args:
        current_page: The current page being displayed
    """
    with st.container():
        # Create the navbar container with CSS class
        st.markdown('<div class="navbar-container">', unsafe_allow_html=True)
        
        # Use columns for layout
        col1, col2 = st.columns([6, 1])
        
        with col1:
            # Create the menu with SAC
            selected = sac.menu(
                items=[
                    sac.MenuItem('home', icon='house-fill'),
                    sac.MenuItem('products', icon='box-fill', children=[
                        sac.MenuItem('apple', icon='apple'),
                        sac.MenuItem('other', icon='diamond-fill', children=[
                            sac.MenuItem('other items')
                        ]),
                        sac.MenuItem('google', icon='google', description='item description'),
                        sac.MenuItem('gitlab', icon='github'),
                        sac.MenuItem('wechat', icon='chat-dots-fill'),
                        sac.MenuItem('disabled', disabled=True),
                    ]),
                    sac.MenuItem(type='divider'),
                    sac.MenuItem('antd-menu', icon='heart-fill'),
                    sac.MenuItem('bootstrap-icon', icon='bootstrap'),
                ],
                format_func='title',
                index=0 if current_page == 'home' else None,
                open_all=False,
                size='md',
            )
            
            # Handle navigation based on selection
            if selected and selected != current_page:
                if selected == 'home':
                    st.switch_page("Home.py")
                elif selected in ['products', 'apple', 'other', 'google', 'gitlab', 'wechat']:
                    # Set filter in session state
                    st.session_state.project_filter = selected
                    st.switch_page("pages/Projects.py")
                elif selected == 'antd-menu':
                    st.session_state.about_section = 'profile'
                    st.switch_page("pages/About.py")
        
        with col2:
            # Add tags/badges on the right side using our CSS classes
            st.markdown("""
            <div style="display: flex; justify-content: flex-end; gap: 8px; margin-top: 5px;">
                <span class="navbar-tag navbar-tag-green">Tag1</span>
                <span class="navbar-tag navbar-tag-red">Tag2</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Add a sidebar toggle button with unique key
            if st.button("☰", key=f"{current_page}_desktop_sidebar_toggle"):
                # Toggle sidebar visibility
                if st.session_state.get("sidebar_visible", True):
                    st.session_state.sidebar_visible = False
                    st.markdown("""
                    <script>
                        var sidebar = window.parent.document.querySelector('[data-testid="stSidebar"]');
                        sidebar.style.display = 'none';
                    </script>
                    """, unsafe_allow_html=True)
                else:
                    st.session_state.sidebar_visible = True
                    st.markdown("""
                    <script>
                        var sidebar = window.parent.document.querySelector('[data-testid="stSidebar"]');
                        sidebar.style.display = 'flex';
                    </script>
                    """, unsafe_allow_html=True)
        
        # Close the navbar container
        st.markdown('</div>', unsafe_allow_html=True)


def add_sidebar_toggle_script():
    """
    Add JavaScript to toggle the sidebar visibility.
    """
    st.markdown("""
    <script>
        // Function to toggle sidebar
        function toggleSidebar() {
            var sidebar = window.parent.document.querySelector('[data-testid="stSidebar"]');
            if (sidebar.style.display === 'none') {
                sidebar.style.display = 'flex';
            } else {
                sidebar.style.display = 'none';
            }
        }
        
        // Add toggle button to navbar
        var navbar = window.parent.document.querySelector('.navbar-container');
        var toggleBtn = document.createElement('button');
        toggleBtn.innerHTML = '☰';
        toggleBtn.className = 'sidebar-toggle';
        toggleBtn.onclick = toggleSidebar;
        navbar.appendChild(toggleBtn);
    </script>
    """, unsafe_allow_html=True)


def initialize_navigation():
    """Initialize navigation settings for the application."""
    # Determine current page based on URL
    current_page = "home"
    
    # Get the script path from sys.argv[0]
    script_path = sys.argv[0] if len(sys.argv) > 0 else ""
    
    if "Projects.py" in script_path:
        current_page = "projects"
    elif "About.py" in script_path:
        current_page = "about"
    
    # Initialize project_filter if not set
    if "project_filter" not in st.session_state:
        st.session_state.project_filter = "all_projects"
    
    # Set default sidebar state if not already set
    if "sidebar_visible" not in st.session_state:
        st.session_state.sidebar_visible = True
    
    # Add CSS for responsive design and JavaScript to remove native sidebar options
    st.markdown("""
    <script>
        // Function to remove native Streamlit sidebar navigation
        function removeNativeSidebarNav() {
            // Target all elements in the sidebar
            const sidebar = window.parent.document.querySelector('[data-testid="stSidebar"]');
            if (sidebar) {
                // Find all navigation elements (the first few elements in the sidebar)
                const elements = sidebar.querySelectorAll('.element-container');
                
                // Remove the first few elements which contain the native navigation
                if (elements.length > 0) {
                    for (let i = 0; i < 3; i++) {  // Remove the first 3 elements (adjust if needed)
                        if (elements[i]) {
                            elements[i].remove();
                        }
                    }
                }
            }
        }
        
        // Run the function after a short delay to ensure the DOM is fully loaded
        setTimeout(removeNativeSidebarNav, 100);
        
        // Also run it when the page changes or reloads
        const observer = new MutationObserver(function(mutations) {
            removeNativeSidebarNav();
        });
        
        // Start observing the document with the configured parameters
        observer.observe(window.parent.document.body, { childList: true, subtree: true });
    </script>
    
    <style>
    /* Style sidebar toggle button */
    .sidebar-toggle {
        background: transparent;
        border: none;
        color: white;
        font-size: 24px;
        cursor: pointer;
        padding: 5px 10px;
        border-radius: 5px;
    }
    
    .sidebar-toggle:hover {
        background-color: rgba(255, 255, 255, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Always use the regular navbar
    create_navbar(current_page)
    
    return current_page


def is_mobile():
    """
    Check if the user is on a mobile device.
    
    Since JavaScript detection is unreliable in Streamlit,
    we'll use a manual approach with a session state variable.
    """
    # Default to desktop view
    if "use_mobile_nav" not in st.session_state:
        st.session_state.use_mobile_nav = False
    
    # Add a toggle in the sidebar for testing
    with st.sidebar:
        st.markdown("---")
        st.markdown("### View Settings")
        mobile_toggle = st.checkbox("Use Mobile Navigation", 
                                   value=st.session_state.use_mobile_nav,
                                   key="mobile_nav_toggle")
        
        # Update session state if toggle changes
        if mobile_toggle != st.session_state.use_mobile_nav:
            st.session_state.use_mobile_nav = mobile_toggle
    
    return st.session_state.use_mobile_nav


def create_mobile_navbar(current_page: str = "home") -> None:
    """
    Create a mobile-friendly navigation bar.
    
    Args:
        current_page: The current page being displayed
    """
    with st.sidebar:
        st.markdown("<h1>Mobile Navigation</h1>", unsafe_allow_html=True)
        
        # Create simple buttons for main navigation
        if st.button("Home", use_container_width=True, key="mobile_home"):
            st.switch_page("Home.py")
            
        if st.button("Projects", use_container_width=True, key="mobile_projects"):
            st.session_state.project_filter = 'all_projects'
            st.switch_page("pages/Projects.py")
            
        if st.button("About", use_container_width=True, key="mobile_about"):
            st.switch_page("pages/About.py")
        
        # Add project filter navigation
        st.markdown("---")
        st.markdown("<h3>Project Categories</h3>", unsafe_allow_html=True)
        
        # Create direct buttons for project filters
        if st.button("All Projects", use_container_width=True, key="mobile_all_projects"):
            st.session_state.project_filter = 'all_projects'
            if current_page != 'projects':
                st.switch_page("pages/Projects.py")
            else:
                st.rerun()
                
        if st.button("Data Science", use_container_width=True, key="mobile_data_science"):
            st.session_state.project_filter = 'data_science'
            if current_page != 'projects':
                st.switch_page("pages/Projects.py")
            else:
                st.rerun()
                
        if st.button("Web Development", use_container_width=True, key="mobile_web_dev"):
            st.session_state.project_filter = 'web_dev'
            if current_page != 'projects':
                st.switch_page("pages/Projects.py")
            else:
                st.rerun()
            