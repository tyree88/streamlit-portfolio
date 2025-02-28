"""
Data processing flows for the Streamlit portfolio.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Tuple
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

from prefect import flow, task, get_run_logger
from prefect.artifacts import create_markdown_artifact
from prefect.tasks import task_input_hash
from datetime import timedelta

from .config import DATA_PROCESSING_FLOW, DATASETS
from .utils import (
    download_dataset,
    load_dataset,
    save_dataset,
    log_flow_run_info,
)


@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(hours=24))
def analyze_dataset(df: pd.DataFrame, dataset_name: str) -> Dict:
    """
    Analyze a dataset and return summary statistics.
    
    Args:
        df: DataFrame to analyze
        dataset_name: Name of the dataset
        
    Returns:
        Dictionary with dataset analysis
    """
    logger = get_run_logger()
    logger.info(f"Analyzing dataset {dataset_name} with shape {df.shape}")
    
    # Basic statistics
    analysis = {
        "dataset_name": dataset_name,
        "shape": df.shape,
        "columns": list(df.columns),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "missing_values": df.isnull().sum().to_dict(),
        "missing_percentage": (df.isnull().sum() / len(df) * 100).to_dict(),
    }
    
    # Numeric columns statistics
    numeric_cols = df.select_dtypes(include=["number"]).columns
    if len(numeric_cols) > 0:
        analysis["numeric_stats"] = {
            col: {
                "min": df[col].min(),
                "max": df[col].max(),
                "mean": df[col].mean(),
                "median": df[col].median(),
                "std": df[col].std(),
            }
            for col in numeric_cols
        }
    
    # Categorical columns statistics
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns
    if len(categorical_cols) > 0:
        analysis["categorical_stats"] = {
            col: {
                "unique_values": df[col].nunique(),
                "top_values": df[col].value_counts().head(5).to_dict(),
            }
            for col in categorical_cols
        }
    
    # Create artifact
    create_markdown_artifact(
        markdown=f"## Dataset Analysis: {dataset_name}\n\n"
                f"- **Shape**: {analysis['shape']}\n"
                f"- **Columns**: {len(analysis['columns'])}\n"
                f"- **Missing Values**: {sum(analysis['missing_values'].values())}\n\n"
                f"### Numeric Columns\n"
                f"{', '.join(numeric_cols)}\n\n"
                f"### Categorical Columns\n"
                f"{', '.join(categorical_cols)}",
        key=f"dataset-analysis-{dataset_name}",
    )
    
    return analysis


@task
def clean_dataset(df: pd.DataFrame, dataset_name: str) -> pd.DataFrame:
    """
    Clean a dataset by handling missing values, duplicates, and outliers.
    
    Args:
        df: DataFrame to clean
        dataset_name: Name of the dataset
        
    Returns:
        Cleaned DataFrame
    """
    logger = get_run_logger()
    logger.info(f"Cleaning dataset {dataset_name}")
    
    # Make a copy to avoid modifying the original
    df_clean = df.copy()
    
    # Remove duplicates
    initial_rows = len(df_clean)
    df_clean = df_clean.drop_duplicates()
    duplicates_removed = initial_rows - len(df_clean)
    logger.info(f"Removed {duplicates_removed} duplicate rows")
    
    # Handle missing values based on dataset
    if dataset_name == "customer_churn":
        # For customer churn dataset
        # Fill missing numeric values with median
        numeric_cols = df_clean.select_dtypes(include=["number"]).columns
        for col in numeric_cols:
            if df_clean[col].isnull().sum() > 0:
                df_clean[col] = df_clean[col].fillna(df_clean[col].median())
        
        # Fill missing categorical values with mode
        categorical_cols = df_clean.select_dtypes(include=["object", "category"]).columns
        for col in categorical_cols:
            if df_clean[col].isnull().sum() > 0:
                df_clean[col] = df_clean[col].fillna(df_clean[col].mode()[0])
    
    elif dataset_name == "housing":
        # For housing dataset
        # Handle specific columns
        if "total_bedrooms" in df_clean.columns and df_clean["total_bedrooms"].isnull().sum() > 0:
            df_clean["total_bedrooms"] = df_clean["total_bedrooms"].fillna(df_clean["total_bedrooms"].median())
    
    # Log missing values after cleaning
    missing_after = df_clean.isnull().sum().sum()
    logger.info(f"Missing values after cleaning: {missing_after}")
    
    # Create artifact
    create_markdown_artifact(
        markdown=f"## Dataset Cleaning: {dataset_name}\n\n"
                f"- **Initial Shape**: {df.shape}\n"
                f"- **Cleaned Shape**: {df_clean.shape}\n"
                f"- **Duplicates Removed**: {duplicates_removed}\n"
                f"- **Missing Values Before**: {df.isnull().sum().sum()}\n"
                f"- **Missing Values After**: {missing_after}",
        key=f"dataset-cleaning-{dataset_name}",
    )
    
    return df_clean


@task
def transform_dataset(df: pd.DataFrame, dataset_name: str) -> pd.DataFrame:
    """
    Transform a dataset by creating new features, encoding categorical variables, etc.
    
    Args:
        df: DataFrame to transform
        dataset_name: Name of the dataset
        
    Returns:
        Transformed DataFrame
    """
    logger = get_run_logger()
    logger.info(f"Transforming dataset {dataset_name}")
    
    # Make a copy to avoid modifying the original
    df_transformed = df.copy()
    
    # Dataset-specific transformations
    if dataset_name == "customer_churn":
        # Convert Yes/No to 1/0 for target variable
        if "Churn" in df_transformed.columns:
            df_transformed["Churn"] = df_transformed["Churn"].map({"Yes": 1, "No": 0})
        
        # Convert categorical Yes/No columns to 1/0
        yes_no_columns = [
            col for col in df_transformed.columns
            if df_transformed[col].dtype == "object" and 
            set(df_transformed[col].dropna().unique()).issubset({"Yes", "No"})
        ]
        
        for col in yes_no_columns:
            df_transformed[col] = df_transformed[col].map({"Yes": 1, "No": 0})
        
        # Convert TotalCharges to numeric
        if "TotalCharges" in df_transformed.columns:
            df_transformed["TotalCharges"] = pd.to_numeric(df_transformed["TotalCharges"], errors="coerce")
            
        # Create tenure groups
        if "tenure" in df_transformed.columns:
            df_transformed["tenure_group"] = pd.cut(
                df_transformed["tenure"],
                bins=[0, 12, 24, 36, 48, 60, 72],
                labels=["0-1 year", "1-2 years", "2-3 years", "3-4 years", "4-5 years", "5+ years"]
            )
    
    elif dataset_name == "housing":
        # Create new features
        if all(col in df_transformed.columns for col in ["total_rooms", "households"]):
            df_transformed["rooms_per_household"] = df_transformed["total_rooms"] / df_transformed["households"]
        
        if all(col in df_transformed.columns for col in ["total_bedrooms", "total_rooms"]):
            df_transformed["bedrooms_ratio"] = df_transformed["total_bedrooms"] / df_transformed["total_rooms"]
        
        if all(col in df_transformed.columns for col in ["population", "households"]):
            df_transformed["population_per_household"] = df_transformed["population"] / df_transformed["households"]
        
        # Log transform skewed features
        if "median_house_value" in df_transformed.columns:
            df_transformed["median_house_value_log"] = np.log1p(df_transformed["median_house_value"])
    
    # Create artifact
    create_markdown_artifact(
        markdown=f"## Dataset Transformation: {dataset_name}\n\n"
                f"- **Initial Shape**: {df.shape}\n"
                f"- **Transformed Shape**: {df_transformed.shape}\n"
                f"- **New Columns**: {set(df_transformed.columns) - set(df.columns)}",
        key=f"dataset-transformation-{dataset_name}",
    )
    
    return df_transformed


@task
def split_dataset(
    df: pd.DataFrame, 
    dataset_name: str,
    test_size: float = 0.2,
    val_size: float = 0.1,
    random_state: int = 42
) -> Dict[str, pd.DataFrame]:
    """
    Split a dataset into train, validation, and test sets.
    
    Args:
        df: DataFrame to split
        dataset_name: Name of the dataset
        test_size: Proportion of data to use for testing
        val_size: Proportion of data to use for validation
        random_state: Random seed for reproducibility
        
    Returns:
        Dictionary with train, validation, and test DataFrames
    """
    logger = get_run_logger()
    logger.info(f"Splitting dataset {dataset_name}")
    
    # Get target variable
    target = DATASETS[dataset_name]["target"]
    
    if target not in df.columns:
        raise ValueError(f"Target column '{target}' not found in dataset")
    
    # Split features and target
    X = df.drop(columns=[target])
    y = df[target]
    
    # First split: train+val and test
    X_train_val, X_test, y_train_val, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y if y.dtype == "object" else None
    )
    
    # Second split: train and validation
    val_ratio = val_size / (1 - test_size)
    X_train, X_val, y_train, y_val = train_test_split(
        X_train_val, y_train_val, test_size=val_ratio, random_state=random_state, 
        stratify=y_train_val if y_train_val.dtype == "object" else None
    )
    
    # Combine features and target
    train_df = pd.concat([X_train, y_train], axis=1)
    val_df = pd.concat([X_val, y_val], axis=1)
    test_df = pd.concat([X_test, y_test], axis=1)
    
    logger.info(f"Train set shape: {train_df.shape}")
    logger.info(f"Validation set shape: {val_df.shape}")
    logger.info(f"Test set shape: {test_df.shape}")
    
    # Create artifact
    create_markdown_artifact(
        markdown=f"## Dataset Split: {dataset_name}\n\n"
                f"- **Original Shape**: {df.shape}\n"
                f"- **Train Shape**: {train_df.shape} ({len(train_df) / len(df):.1%})\n"
                f"- **Validation Shape**: {val_df.shape} ({len(val_df) / len(df):.1%})\n"
                f"- **Test Shape**: {test_df.shape} ({len(test_df) / len(df):.1%})\n"
                f"- **Target Column**: {target}",
        key=f"dataset-split-{dataset_name}",
    )
    
    return {
        "train": train_df,
        "val": val_df,
        "test": test_df,
    }


@flow(
    name=DATA_PROCESSING_FLOW.name,
    description=DATA_PROCESSING_FLOW.description,
    retries=DATA_PROCESSING_FLOW.retries,
    retry_delay_seconds=DATA_PROCESSING_FLOW.retry_delay_seconds,
    log_prints=DATA_PROCESSING_FLOW.log_prints,
)
def load_and_process_data(
    dataset_name: str,
    force_download: bool = False,
    test_size: float = 0.2,
    val_size: float = 0.1,
    random_state: int = 42,
) -> Dict[str, Path]:
    """
    Load and process a dataset for analysis and modeling.
    
    Args:
        dataset_name: Name of the dataset to process
        force_download: Whether to force download even if file exists
        test_size: Proportion of data to use for testing
        val_size: Proportion of data to use for validation
        random_state: Random seed for reproducibility
        
    Returns:
        Dictionary with paths to the processed datasets
    """
    # Log flow run info
    log_flow_run_info()
    
    # Download and load dataset
    dataset_path = download_dataset(dataset_name, force_download)
    df = load_dataset(dataset_path)
    
    # Analyze dataset
    analysis = analyze_dataset(df, dataset_name)
    
    # Clean dataset
    df_clean = clean_dataset(df, dataset_name)
    
    # Transform dataset
    df_transformed = transform_dataset(df_clean, dataset_name)
    
    # Split dataset
    splits = split_dataset(
        df_transformed, 
        dataset_name,
        test_size=test_size,
        val_size=val_size,
        random_state=random_state
    )
    
    # Save processed datasets
    paths = {}
    for split_name, split_df in splits.items():
        path = save_dataset(split_df, dataset_name, suffix=f"{split_name}")
        paths[split_name] = path
    
    return paths


if __name__ == "__main__":
    # Run the flow for a specific dataset
    load_and_process_data("customer_churn") 