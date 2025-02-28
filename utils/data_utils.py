"""
Data loading and processing utilities.
"""

import os
import json
import pandas as pd
from typing import Dict, List, Any, Optional


def load_data(file_path: str) -> Any:
    """
    Load data from various file formats.
    
    Args:
        file_path: Path to the data file
        
    Returns:
        Loaded data in appropriate format
    """
    _, ext = os.path.splitext(file_path)
    
    if ext.lower() == '.csv':
        return pd.read_csv(file_path)
    elif ext.lower() == '.json':
        with open(file_path, 'r') as f:
            return json.load(f)
    elif ext.lower() in ['.xlsx', '.xls']:
        return pd.read_excel(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")


def filter_projects(projects: List[Dict], 
                   tags: Optional[List[str]] = None, 
                   search_term: Optional[str] = None) -> List[Dict]:
    """
    Filter projects based on tags and search term.
    
    Args:
        projects: List of project dictionaries
        tags: List of tags to filter by
        search_term: Search term to filter by
        
    Returns:
        Filtered list of projects
    """
    filtered_projects = projects
    
    if tags:
        filtered_projects = [
            project for project in filtered_projects
            if any(tag in project.get('tags', []) for tag in tags)
        ]
    
    if search_term:
        search_term = search_term.lower()
        filtered_projects = [
            project for project in filtered_projects
            if search_term in project.get('title', '').lower() or
               search_term in project.get('description', '').lower()
        ]
    
    return filtered_projects


def prepare_skills_data(skills: List[Dict]) -> pd.DataFrame:
    """
    Prepare skills data for visualization.
    
    Args:
        skills: List of skill dictionaries with 'name' and 'level'
        
    Returns:
        DataFrame with prepared skills data
    """
    df = pd.DataFrame(skills)
    
    # Ensure the DataFrame has the required columns
    if 'name' not in df.columns or 'level' not in df.columns:
        raise ValueError("Skills data must contain 'name' and 'level' columns")
    
    # Sort by skill level (descending)
    df = df.sort_values('level', ascending=False)
    
    # Add category based on level
    df['category'] = pd.cut(
        df['level'],
        bins=[0, 40, 70, 100],
        labels=['Beginner', 'Intermediate', 'Advanced']
    )
    
    return df 