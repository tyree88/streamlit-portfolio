"""
Configuration settings for the Streamlit portfolio application.
"""

# Site configuration
SITE_CONFIG = {
    "title": "My Portfolio",
    "subtitle": "Data Scientist & Developer",
    "icon": "🚀",
    "author": "Your Name",
    "email": "your.email@example.com",
    "github": "https://github.com/yourusername",
    "linkedin": "https://linkedin.com/in/yourusername",
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
        {"name": "SQL", "level": 85},
        {"name": "Streamlit", "level": 90},
    ],
    "education": [
        {
            "degree": "Master of Science in Data Science",
            "institution": "University Name",
            "year": "2020-2022",
            "description": "Focused on machine learning and data visualization."
        },
        {
            "degree": "Bachelor of Science in Computer Science",
            "institution": "University Name",
            "year": "2016-2020",
            "description": "Specialized in software engineering and algorithms."
        }
    ],
    "experience": [
        {
            "title": "Data Scientist",
            "company": "Company Name",
            "period": "2022-Present",
            "description": "Developed machine learning models for predictive analytics."
        },
        {
            "title": "Software Developer",
            "company": "Company Name",
            "period": "2020-2022",
            "description": "Built web applications and data pipelines."
        }
    ]
}

# API keys and sensitive information (use environment variables in production)
# import os
# API_KEYS = {
#     "openai": os.environ.get("OPENAI_API_KEY"),
#     "github": os.environ.get("GITHUB_TOKEN"),
# } 