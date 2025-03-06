# Streamlit Portfolio

A professional portfolio application built with Streamlit and enhanced with modern UI components from streamlit-shadcn-ui.

## Project Structure

```
streamlit-portfolio/
├── Home.py                 # Main application entry point
├── config.py               # Configuration settings
├── requirements.txt        # Project dependencies
├── .streamlit/             # Streamlit configuration
│   └── config.toml         # Streamlit theme and settings
├── assets/                 # Static assets
│   ├── css/                # Custom CSS
│   │   ├── pages/          # Page-specific CSS
│   │   │   ├── common.css  # Shared styles
│   │   │   ├── home.css    # Home page styles
│   │   │   ├── about.css   # About page styles
│   │   │   └── projects.css # Projects page styles
│   └── images/             # Images used in the app
├── components/             # Reusable UI components
│   ├── footer.py           # Footer component
│   ├── navbar.py           # Navigation bar
│   ├── contact_form.py     # Contact form component
│   ├── social_links.py     # Social media links
│   └── ...
├── data/                   # Data files and datasets
├── pages/                  # Multi-page app sections
│   ├── About.py            # About page
│   └── Projects.py         # Projects page
├── utils/                  # Utility functions
│   ├── display_utils.py    # Display utilities
│   ├── data_utils.py       # Data processing utilities
│   └── github_utils.py     # GitHub API integration
└── tests/                  # Unit and integration tests
```

## Setup

1. Clone the repository
2. Install UV (if not already installed):
   ```bash
   curl -sSf https://install.ultraviolet.rs | sh
   ```
   Or with pip:
   ```bash
   pip install uv
   ```
3. Create a virtual environment and install dependencies in one step:
   ```bash
   uv venv .venv
   ```
4. Activate the virtual environment:
   - Windows: `.venv\Scripts\activate`
   - macOS/Linux: `source .venv/bin/activate`
5. Install dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```
6. Run the application:
   ```bash
   streamlit run Home.py
   ```

## Features

- Modern, responsive dark theme design
- Multi-page navigation with streamlit-shadcn-ui components
- Project showcase with filtering and search
- Social media integration
- Skills visualization with interactive charts
- Timeline components for education and experience
- GitHub repository integration

## Recent Improvements

### UI Enhancements
- Improved badge styling for better visibility on dark backgrounds
- Increased text sizes for better readability
- Added consistent card styling with hover effects
- Modernized button styling with transitions
- Enhanced timeline components with custom styling

### Code Improvements
- Consolidated duplicate functions
- Improved component reusability
- Enhanced CSS organization with variables
- Optimized styling for better performance
- Consistent styling across all pages

## Development

### Adding a New Page

1. Create a new Python file in the `pages/` directory
2. Implement the page content using Streamlit components
3. Add corresponding CSS in `assets/css/pages/` if needed

### Adding Dependencies

To add new dependencies:

1. Add the package to `requirements.txt`
2. Install it with UV:
   ```bash
   uv pip install -r requirements.txt
   ```

### Styling

Custom styling is implemented through:
1. CSS variables in `assets/css/pages/common.css`
2. Page-specific styles in `assets/css/pages/`
3. Component-specific styling in the Python files

The portfolio uses a consistent dark theme with accent colors that can be customized in the CSS variables.
