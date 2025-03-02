"""
Components package for the Streamlit portfolio.
"""

from components.footer import create_footer
from components.contact_form import contact_info
from components.navbar import create_navbar
from components.project_card import create_project_card, create_featured_projects
from components.skill_card import create_skill_card, create_skills_section
from components.social_links import create_social_badges, create_social_buttons
from components.page_header import setup_page, create_page_header, create_sidebar_profile
from components.theme_setup import load_css, add_custom_fonts, add_font_awesome
from components.github_repo_card import create_repo_card, create_github_repos_section
from components.hero_section import create_hero_section
from components.profile_card import create_profile_card
from components.timeline import (
    create_timeline_item, 
    create_timeline, 
    create_experience_section, 
    create_education_section
)
from components.call_to_action import create_call_to_action 