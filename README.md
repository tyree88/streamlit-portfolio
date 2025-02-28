# Streamlit Portfolio

A professional portfolio application built with Streamlit.

## Project Structure

```
streamlit-portfolio/
├── app.py                  # Main application entry point
├── config.py               # Configuration settings
├── requirements.txt        # Project dependencies
├── .streamlit/             # Streamlit configuration
│   └── config.toml         # Streamlit theme and settings
├── assets/                 # Static assets
│   ├── css/                # Custom CSS
│   └── images/             # Images used in the app
├── components/             # Reusable UI components
│   └── __init__.py
├── data/                   # Data files and datasets
│   └── __init__.py
├── pages/                  # Multi-page app sections
│   ├── __init__.py
│   ├── 01_about.py
│   ├── 02_projects.py
│   └── 03_contact.py
├── services/               # External API integrations
│   └── __init__.py
├── utils/                  # Utility functions
│   └── __init__.py
└── tests/                  # Unit and integration tests
    └── __init__.py
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
   streamlit run app.py
   ```

## Features

- Responsive design
- Multi-page navigation
- Project showcase
- Contact form
- Skills visualization
- Data visualization with Prefect workflows
- ETL pipelines for data processing
- Machine learning model training and evaluation

## Development

### Adding a New Page

1. Create a new Python file in the `pages/` directory
2. Name it with a number prefix to control the order (e.g., `04_new_page.py`)
3. Implement the page content using Streamlit components

### Adding Dependencies

To add new dependencies:

1. Add the package to `requirements.txt`
2. Install it with UV:
   ```bash
   uv pip install -r requirements.txt
   ```

### Styling

Custom styling can be added in the `.streamlit/config.toml` file or in CSS files in the `assets/css/` directory.
