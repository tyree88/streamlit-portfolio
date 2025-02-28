"""
Prefect flows for the Streamlit portfolio application.

This package contains all the Prefect flows that power the data processing
and machine learning pipelines showcased in the portfolio.
"""

from .data_flows import load_and_process_data
from .ml_flows import train_model, evaluate_model
from .etl_flows import extract_transform_load
from .visualization_flows import generate_visualizations 