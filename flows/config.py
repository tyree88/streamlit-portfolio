"""
Configuration settings for Prefect flows.
"""

import os
from pathlib import Path
from pydantic import BaseModel
from typing import Dict, List, Optional, Union

# Base directory for data
BASE_DATA_DIR = Path("data")
PROCESSED_DATA_DIR = BASE_DATA_DIR / "processed"
RAW_DATA_DIR = BASE_DATA_DIR / "raw"
MODEL_DIR = Path("models")

# Ensure directories exist
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

# Flow configurations
class FlowConfig(BaseModel):
    """Base configuration for flows."""
    name: str
    description: str
    tags: List[str]
    retries: int = 3
    retry_delay_seconds: int = 60
    timeout_seconds: Optional[int] = None
    log_prints: bool = True


# Project-specific flow configurations
DATA_PROCESSING_FLOW = FlowConfig(
    name="data-processing",
    description="Load and process data for analysis and modeling",
    tags=["data", "processing", "portfolio"],
)

ML_TRAINING_FLOW = FlowConfig(
    name="ml-training",
    description="Train machine learning models on processed data",
    tags=["ml", "training", "portfolio"],
)

ML_EVALUATION_FLOW = FlowConfig(
    name="ml-evaluation",
    description="Evaluate machine learning models and generate metrics",
    tags=["ml", "evaluation", "portfolio"],
)

ETL_FLOW = FlowConfig(
    name="etl-pipeline",
    description="Extract, transform, and load data from various sources",
    tags=["etl", "data", "portfolio"],
)

VISUALIZATION_FLOW = FlowConfig(
    name="data-visualization",
    description="Generate visualizations from processed data",
    tags=["visualization", "data", "portfolio"],
)

# Dataset configurations
DATASETS = {
    "customer_churn": {
        "filename": "customer_churn.csv",
        "url": "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv",
        "description": "Telco customer churn dataset",
        "target": "Churn",
    },
    "housing": {
        "filename": "housing.csv",
        "url": "https://raw.githubusercontent.com/ageron/handson-ml2/master/datasets/housing/housing.csv",
        "description": "California housing dataset",
        "target": "median_house_value",
    },
    "iris": {
        "filename": "iris.csv",
        "url": "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv",
        "description": "Iris flower dataset",
        "target": "species",
    },
}

# Model configurations
MODELS = {
    "customer_churn": {
        "algorithms": ["random_forest", "gradient_boosting", "logistic_regression"],
        "metrics": ["accuracy", "precision", "recall", "f1", "roc_auc"],
        "cv_folds": 5,
    },
    "housing": {
        "algorithms": ["random_forest", "gradient_boosting", "linear_regression"],
        "metrics": ["rmse", "mae", "r2"],
        "cv_folds": 5,
    },
    "iris": {
        "algorithms": ["random_forest", "svm", "knn"],
        "metrics": ["accuracy", "precision", "recall", "f1"],
        "cv_folds": 5,
    },
}

# Prefect deployment settings
DEPLOYMENT_SETTINGS = {
    "work_queue_name": "portfolio",
    "interval_seconds": 3600 * 24,  # Daily
} 