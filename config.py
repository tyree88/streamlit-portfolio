"""
Configuration settings for the Streamlit portfolio application.
"""



# Site configuration
SITE_CONFIG = {
    "title": "My Portfolio",
    "subtitle": "Data Scientist & Developer",
    "description": "I'm a data scientist and developer with a passion for building innovative solutions. I love solving complex problems and building innovative solutions.",
    "icon": "🚀",
    "author": "Tyree Pearson",
    "github": "https://github.com/tyree88",
    "linkedin": "https://linkedin.com/in/tyreepearson",
    "bluesky": "https://bsky.app/profile/tyrendie.bsky.social",
}

# Theme configuration
THEME_CONFIG = {
    "primary_color": "#4257b2",
    "secondary_color": "#5c88da",
    "text_color": "#333333",
    "background_color": "#ffffff",
}

# Content configuration
CONTENT_CONFIG = {
    "skills": [
        {"name": "Python", "level": 90},
        {"name": "Data Analysis", "level": 85},
        {"name": "Machine Learning", "level": 80},
        {"name": "Web Development", "level": 75},
        {"name": "Streamlit", "level": 90},
    ],
    "education": [
        {
            "degree": "Applied Generative AI Certificate",
            "institution": "Johns Hopkins University",
            "year": "2025",
            "description": "Focused on Generative AI and its applications."
        },
        {
            "degree": "Bachelor of Science in Geography",
            "institution": "University of Texas at Austin",
            "year": "2015-2019",
            "description": "Majored in Geographic Information Systems and focused on remote sensing and spatial analysis with a minor in Computer Science."
        }
    ],
    "experience": [
        {
            "title": "Solutions Architect",
            "company": "Prefect",
            "period": "2024-Present",
            "description": "Building data pipelines and automating workflows showcasing the power of Prefect."
        },
        {
            "title": "Solutions Architect",
            "company": "Akeyless",
            "period": "2023-2024",
            "description": "Demonstrating the power of Akeyless to secure and manage secrets."
        }
    ]
}

# API keys and sensitive information (use environment variables in production)
# import os
# API_KEYS = {
#     "openai": os.environ.get("OPENAI_API_KEY"),
#     "github": os.environ.get("GITHUB_TOKEN"),
# } 