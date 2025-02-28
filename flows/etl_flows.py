"""
ETL flows for the Streamlit portfolio.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Tuple
import requests
import json
import os
from datetime import datetime, timedelta
import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from prefect import flow, task, get_run_logger
from prefect.artifacts import create_markdown_artifact
from prefect.tasks import task_input_hash
from prefect_sqlalchemy import SqlAlchemyConnector

from .config import ETL_FLOW, DATASETS
from .utils import (
    download_dataset,
    load_dataset,
    save_dataset,
    log_flow_run_info,
)


@task(retries=3, retry_delay_seconds=10)
def extract_data(
    source_type: str,
    source_path: Optional[str] = None,
    source_url: Optional[str] = None,
    source_query: Optional[str] = None,
    source_db: Optional[str] = None,
    dataset_name: Optional[str] = None,
) -> pd.DataFrame:
    """
    Extract data from various sources.
    
    Args:
        source_type: Type of source (file, url, database, api)
        source_path: Path to the source file
        source_url: URL to the source data
        source_query: SQL query for database source
        source_db: Database connection string
        dataset_name: Name of the dataset (for predefined datasets)
        
    Returns:
        DataFrame with extracted data
    """
    logger = get_run_logger()
    logger.info(f"Extracting data from {source_type} source")
    
    if source_type == "file" and source_path:
        # Extract from local file
        logger.info(f"Loading data from file: {source_path}")
        return pd.read_csv(source_path)
    
    elif source_type == "url" and source_url:
        # Extract from URL
        logger.info(f"Downloading data from URL: {source_url}")
        response = requests.get(source_url)
        response.raise_for_status()
        
        # Determine file type from URL
        if source_url.endswith(".csv"):
            return pd.read_csv(pd.io.common.StringIO(response.text))
        elif source_url.endswith(".json"):
            return pd.DataFrame(response.json())
        else:
            # Default to CSV
            return pd.read_csv(pd.io.common.StringIO(response.text))
    
    elif source_type == "database" and source_query and source_db:
        # Extract from database
        logger.info(f"Executing query on database: {source_db}")
        
        # Use SQLAlchemy connector
        connector = SqlAlchemyConnector.load("portfolio-db")
        with connector.get_connection() as engine:
            return pd.read_sql(source_query, engine)
    
    elif source_type == "dataset" and dataset_name:
        # Extract from predefined dataset
        logger.info(f"Loading predefined dataset: {dataset_name}")
        dataset_path = download_dataset(dataset_name)
        return load_dataset(dataset_path)
    
    else:
        raise ValueError(f"Invalid source configuration for type: {source_type}")


@task
def transform_data(
    df: pd.DataFrame,
    transformations: List[Dict],
) -> pd.DataFrame:
    """
    Apply a series of transformations to the data.
    
    Args:
        df: DataFrame to transform
        transformations: List of transformation configurations
        
    Returns:
        Transformed DataFrame
    """
    logger = get_run_logger()
    logger.info(f"Applying {len(transformations)} transformations to data")
    
    # Make a copy to avoid modifying the original
    df_transformed = df.copy()
    
    # Apply each transformation
    for i, transform in enumerate(transformations):
        transform_type = transform.get("type")
        logger.info(f"Applying transformation {i+1}/{len(transformations)}: {transform_type}")
        
        if transform_type == "drop_columns":
            # Drop specified columns
            columns = transform.get("columns", [])
            df_transformed = df_transformed.drop(columns=columns)
        
        elif transform_type == "rename_columns":
            # Rename columns
            rename_map = transform.get("mapping", {})
            df_transformed = df_transformed.rename(columns=rename_map)
        
        elif transform_type == "fill_missing":
            # Fill missing values
            columns = transform.get("columns", df_transformed.columns)
            method = transform.get("method", "mean")
            value = transform.get("value")
            
            for col in columns:
                if col in df_transformed.columns:
                    if method == "mean" and pd.api.types.is_numeric_dtype(df_transformed[col]):
                        df_transformed[col] = df_transformed[col].fillna(df_transformed[col].mean())
                    elif method == "median" and pd.api.types.is_numeric_dtype(df_transformed[col]):
                        df_transformed[col] = df_transformed[col].fillna(df_transformed[col].median())
                    elif method == "mode":
                        df_transformed[col] = df_transformed[col].fillna(df_transformed[col].mode()[0])
                    elif method == "value" and value is not None:
                        df_transformed[col] = df_transformed[col].fillna(value)
        
        elif transform_type == "create_feature":
            # Create new feature
            feature_name = transform.get("name")
            expression = transform.get("expression")
            
            if feature_name and expression:
                # Use eval to apply the expression
                df_transformed[feature_name] = df_transformed.eval(expression)
        
        elif transform_type == "filter_rows":
            # Filter rows based on condition
            condition = transform.get("condition")
            if condition:
                df_transformed = df_transformed.query(condition)
        
        elif transform_type == "encode_categorical":
            # Encode categorical variables
            columns = transform.get("columns", [])
            method = transform.get("method", "one_hot")
            
            if method == "one_hot":
                for col in columns:
                    if col in df_transformed.columns:
                        dummies = pd.get_dummies(df_transformed[col], prefix=col)
                        df_transformed = pd.concat([df_transformed, dummies], axis=1)
                        df_transformed = df_transformed.drop(columns=[col])
            
            elif method == "label":
                for col in columns:
                    if col in df_transformed.columns:
                        df_transformed[col] = df_transformed[col].astype("category").cat.codes
        
        elif transform_type == "normalize":
            # Normalize numeric columns
            columns = transform.get("columns", df_transformed.select_dtypes(include=["number"]).columns)
            method = transform.get("method", "minmax")
            
            for col in columns:
                if col in df_transformed.columns and pd.api.types.is_numeric_dtype(df_transformed[col]):
                    if method == "minmax":
                        min_val = df_transformed[col].min()
                        max_val = df_transformed[col].max()
                        df_transformed[col] = (df_transformed[col] - min_val) / (max_val - min_val)
                    elif method == "zscore":
                        mean_val = df_transformed[col].mean()
                        std_val = df_transformed[col].std()
                        df_transformed[col] = (df_transformed[col] - mean_val) / std_val
        
        elif transform_type == "custom_python":
            # Apply custom Python function
            code = transform.get("code")
            if code:
                # Create a function from the code
                local_vars = {"df": df_transformed}
                exec(code, globals(), local_vars)
                df_transformed = local_vars["df"]
    
    # Log transformation results
    logger.info(f"Transformation complete. Shape: {df_transformed.shape}")
    
    # Create artifact
    create_markdown_artifact(
        markdown=f"## Data Transformation\n\n"
                f"- **Initial Shape**: {df.shape}\n"
                f"- **Transformed Shape**: {df_transformed.shape}\n"
                f"- **Columns Added**: {set(df_transformed.columns) - set(df.columns)}\n"
                f"- **Columns Removed**: {set(df.columns) - set(df_transformed.columns)}\n"
                f"- **Transformations Applied**: {len(transformations)}",
        key=f"etl-transformation-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
    )
    
    return df_transformed


@task
def load_data_to_destination(
    df: pd.DataFrame,
    destination_type: str,
    destination_path: Optional[str] = None,
    destination_table: Optional[str] = None,
    destination_db: Optional[str] = None,
    if_exists: str = "replace",
) -> str:
    """
    Load data to a destination.
    
    Args:
        df: DataFrame to load
        destination_type: Type of destination (file, database)
        destination_path: Path to the destination file
        destination_table: Table name for database destination
        destination_db: Database connection string
        if_exists: What to do if the destination exists (replace, append, fail)
        
    Returns:
        Path or identifier of the loaded data
    """
    logger = get_run_logger()
    logger.info(f"Loading data to {destination_type} destination")
    
    if destination_type == "file" and destination_path:
        # Load to file
        logger.info(f"Saving data to file: {destination_path}")
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        
        # Determine file type from extension
        file_extension = os.path.splitext(destination_path)[1].lower()
        
        if file_extension == ".csv":
            df.to_csv(destination_path, index=False)
        elif file_extension == ".json":
            df.to_json(destination_path, orient="records", indent=2)
        elif file_extension in [".xlsx", ".xls"]:
            df.to_excel(destination_path, index=False)
        elif file_extension == ".parquet":
            df.to_parquet(destination_path, index=False)
        else:
            # Default to CSV
            destination_path = f"{os.path.splitext(destination_path)[0]}.csv"
            df.to_csv(destination_path, index=False)
        
        return destination_path
    
    elif destination_type == "database" and destination_table and destination_db:
        # Load to database
        logger.info(f"Loading data to database table: {destination_table}")
        
        # Use SQLAlchemy connector
        connector = SqlAlchemyConnector.load("portfolio-db")
        with connector.get_connection() as engine:
            df.to_sql(destination_table, engine, if_exists=if_exists, index=False)
        
        return f"{destination_db}/{destination_table}"
    
    else:
        raise ValueError(f"Invalid destination configuration for type: {destination_type}")


@flow(
    name=ETL_FLOW.name,
    description=ETL_FLOW.description,
    retries=ETL_FLOW.retries,
    retry_delay_seconds=ETL_FLOW.retry_delay_seconds,
    log_prints=ETL_FLOW.log_prints,
)
def extract_transform_load(
    source_type: str,
    destination_type: str,
    transformations: List[Dict] = None,
    source_path: Optional[str] = None,
    source_url: Optional[str] = None,
    source_query: Optional[str] = None,
    source_db: Optional[str] = None,
    dataset_name: Optional[str] = None,
    destination_path: Optional[str] = None,
    destination_table: Optional[str] = None,
    destination_db: Optional[str] = None,
    if_exists: str = "replace",
) -> str:
    """
    Extract, transform, and load data from various sources to destinations.
    
    Args:
        source_type: Type of source (file, url, database, api, dataset)
        destination_type: Type of destination (file, database)
        transformations: List of transformation configurations
        source_path: Path to the source file
        source_url: URL to the source data
        source_query: SQL query for database source
        source_db: Database connection string for source
        dataset_name: Name of the dataset (for predefined datasets)
        destination_path: Path to the destination file
        destination_table: Table name for database destination
        destination_db: Database connection string for destination
        if_exists: What to do if the destination exists (replace, append, fail)
        
    Returns:
        Path or identifier of the loaded data
    """
    # Log flow run info
    flow_info = log_flow_run_info()
    
    # Extract data
    df = extract_data(
        source_type=source_type,
        source_path=source_path,
        source_url=source_url,
        source_query=source_query,
        source_db=source_db,
        dataset_name=dataset_name,
    )
    
    # Transform data if transformations are provided
    if transformations:
        df = transform_data(df, transformations)
    
    # Load data to destination
    result = load_data_to_destination(
        df=df,
        destination_type=destination_type,
        destination_path=destination_path,
        destination_table=destination_table,
        destination_db=destination_db,
        if_exists=if_exists,
    )
    
    # Create summary artifact
    create_markdown_artifact(
        markdown=f"## ETL Flow Summary\n\n"
                f"- **Source Type**: {source_type}\n"
                f"- **Destination Type**: {destination_type}\n"
                f"- **Records Processed**: {len(df)}\n"
                f"- **Columns**: {len(df.columns)}\n"
                f"- **Transformations Applied**: {len(transformations) if transformations else 0}\n"
                f"- **Result**: {result}\n"
                f"- **Timestamp**: {datetime.now().isoformat()}",
        key=f"etl-summary-{flow_info['flow_run_id']}",
    )
    
    return result


if __name__ == "__main__":
    # Example usage
    transformations = [
        {
            "type": "rename_columns",
            "mapping": {
                "customerID": "customer_id",
                "gender": "gender",
                "SeniorCitizen": "is_senior",
                "Partner": "has_partner",
                "Dependents": "has_dependents",
                "tenure": "tenure_months",
                "PhoneService": "has_phone_service",
                "MultipleLines": "has_multiple_lines",
                "InternetService": "internet_service_type",
                "OnlineSecurity": "has_online_security",
                "OnlineBackup": "has_online_backup",
                "DeviceProtection": "has_device_protection",
                "TechSupport": "has_tech_support",
                "StreamingTV": "has_streaming_tv",
                "StreamingMovies": "has_streaming_movies",
                "Contract": "contract_type",
                "PaperlessBilling": "has_paperless_billing",
                "PaymentMethod": "payment_method",
                "MonthlyCharges": "monthly_charges",
                "TotalCharges": "total_charges",
                "Churn": "has_churned"
            }
        },
        {
            "type": "fill_missing",
            "columns": ["total_charges"],
            "method": "median"
        },
        {
            "type": "create_feature",
            "name": "avg_monthly_charges",
            "expression": "total_charges / tenure_months"
        }
    ]
    
    extract_transform_load(
        source_type="dataset",
        dataset_name="customer_churn",
        destination_type="file",
        destination_path="data/processed/customer_churn_etl.csv",
        transformations=transformations
    ) 