"""
Tests for utility functions.
"""

import unittest
import pandas as pd
from utils.data_utils import filter_projects, prepare_skills_data


class TestDataUtils(unittest.TestCase):
    """Test cases for data utility functions."""
    
    def test_filter_projects_by_tags(self):
        """Test filtering projects by tags."""
        projects = [
            {"title": "Project 1", "tags": ["Python", "Streamlit"]},
            {"title": "Project 2", "tags": ["Python", "Flask"]},
            {"title": "Project 3", "tags": ["JavaScript", "React"]}
        ]
        
        filtered = filter_projects(projects, tags=["Python"])
        self.assertEqual(len(filtered), 2)
        self.assertEqual(filtered[0]["title"], "Project 1")
        self.assertEqual(filtered[1]["title"], "Project 2")
        
        filtered = filter_projects(projects, tags=["React"])
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["title"], "Project 3")
        
        filtered = filter_projects(projects, tags=["Django"])
        self.assertEqual(len(filtered), 0)
    
    def test_filter_projects_by_search_term(self):
        """Test filtering projects by search term."""
        projects = [
            {"title": "Data Analysis", "description": "A project about data analysis"},
            {"title": "Web App", "description": "A web application"},
            {"title": "Machine Learning", "description": "A machine learning model"}
        ]
        
        filtered = filter_projects(projects, search_term="data")
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["title"], "Data Analysis")
        
        filtered = filter_projects(projects, search_term="app")
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["title"], "Web App")
        
        filtered = filter_projects(projects, search_term="model")
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["title"], "Machine Learning")
        
        filtered = filter_projects(projects, search_term="nonexistent")
        self.assertEqual(len(filtered), 0)
    
    def test_prepare_skills_data(self):
        """Test preparing skills data for visualization."""
        skills = [
            {"name": "Python", "level": 90},
            {"name": "JavaScript", "level": 75},
            {"name": "SQL", "level": 85},
            {"name": "HTML", "level": 60}
        ]
        
        df = prepare_skills_data(skills)
        
        # Check if DataFrame has the right columns
        self.assertIn("name", df.columns)
        self.assertIn("level", df.columns)
        self.assertIn("category", df.columns)
        
        # Check if sorting works
        self.assertEqual(df.iloc[0]["name"], "Python")
        self.assertEqual(df.iloc[-1]["name"], "HTML")
        
        # Check if categorization works
        self.assertEqual(df[df["name"] == "Python"]["category"].iloc[0], "Advanced")
        self.assertEqual(df[df["name"] == "JavaScript"]["category"].iloc[0], "Intermediate")
        self.assertEqual(df[df["name"] == "HTML"]["category"].iloc[0], "Intermediate")


if __name__ == "__main__":
    unittest.main() 