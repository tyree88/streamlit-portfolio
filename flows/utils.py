"""
Utility functions for Prefect flows.
"""

import os
import json
import pandas as pd
import numpy as np
import requests
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Tuple
from datetime import datetime
import joblib
from prefect import task, get_run_logger
from prefect.artifacts import create_markdown_artifact
from prefect.context import get_run_context

from .config import RAW_DATA_DIR, PROCESSED_DATA_DIR, MODEL_DIR, DATASETS


@task(retries=3, retry_delay_seconds=30)
def download_dataset(dataset_name: str, force_download: bool = False) -> Path:
    """
    Download a dataset if it doesn't exist locally.
    
    Args:
        dataset_name: Name of the dataset to download
        force_download: Whether to force download even if file exists
        
    Returns:
        Path to the downloaded dataset
    """
    logger = get_run_logger()
    
    if dataset_name not in DATASETS:
        raise ValueError(f"Dataset {dataset_name} not found in configuration")
    
    dataset_config = DATASETS[dataset_name]
    filename = dataset_config["filename"]
    url = dataset_config["url"]
    
    output_path = RAW_DATA_DIR / filename
    
    # Check if file already exists
    if output_path.exists() and not force_download:
        logger.info(f"Dataset {dataset_name} already exists at {output_path}")
        return output_path
    
    # Download the file
    logger.info(f"Downloading dataset {dataset_name} from {url}")
    response = requests.get(url)
    response.raise_for_status()
    
    # Save the file
    with open(output_path, "wb") as f:
        f.write(response.content)
    
    logger.info(f"Dataset {dataset_name} downloaded to {output_path}")
    
    # Create artifact
    create_markdown_artifact(
        markdown=f"## Dataset Downloaded\n\n"
                f"- **Name**: {dataset_name}\n"
                f"- **Source**: {url}\n"
                f"- **Destination**: {output_path}\n"
                f"- **Size**: {len(response.content) / 1024:.2f} KB\n"
                f"- **Timestamp**: {datetime.now().isoformat()}",
        key=f"dataset-download-{dataset_name}",
    )
    
    return output_path


@task
def load_dataset(dataset_path: Path) -> pd.DataFrame:
    """
    Load a dataset from a file.
    
    Args:
        dataset_path: Path to the dataset file
        
    Returns:
        Loaded DataFrame
    """
    logger = get_run_logger()
    logger.info(f"Loading dataset from {dataset_path}")
    
    # Determine file type from extension
    file_extension = dataset_path.suffix.lower()
    
    if file_extension == ".csv":
        df = pd.read_csv(dataset_path)
    elif file_extension in [".xlsx", ".xls"]:
        df = pd.read_excel(dataset_path)
    elif file_extension == ".json":
        df = pd.read_json(dataset_path)
    elif file_extension == ".parquet":
        df = pd.read_parquet(dataset_path)
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")
    
    logger.info(f"Loaded dataset with shape {df.shape}")
    
    # Create artifact
    create_markdown_artifact(
        markdown=f"## Dataset Loaded\n\n"
                f"- **Path**: {dataset_path}\n"
                f"- **Shape**: {df.shape}\n"
                f"- **Columns**: {', '.join(df.columns)}\n"
                f"- **Timestamp**: {datetime.now().isoformat()}",
        key=f"dataset-load-{dataset_path.stem}",
    )
    
    return df


@task
def save_dataset(df: pd.DataFrame, dataset_name: str, suffix: str = "processed") -> Path:
    """
    Save a DataFrame to a file.
    
    Args:
        df: DataFrame to save
        dataset_name: Name of the dataset
        suffix: Suffix to add to the filename
        
    Returns:
        Path to the saved dataset
    """
    logger = get_run_logger()
    
    # Create filename
    filename = f"{dataset_name}_{suffix}.csv"
    output_path = PROCESSED_DATA_DIR / filename
    
    logger.info(f"Saving dataset to {output_path}")
    df.to_csv(output_path, index=False)
    
    # Create artifact
    create_markdown_artifact(
        markdown=f"## Dataset Saved\n\n"
                f"- **Name**: {dataset_name}\n"
                f"- **Path**: {output_path}\n"
                f"- **Shape**: {df.shape}\n"
                f"- **Timestamp**: {datetime.now().isoformat()}",
        key=f"dataset-save-{dataset_name}-{suffix}",
    )
    
    return output_path


@task
def save_model(model: Any, model_name: str, dataset_name: str, metadata: Dict = None) -> Path:
    """
    Save a trained model to disk.
    
    Args:
        model: Trained model to save
        model_name: Name of the model
        dataset_name: Name of the dataset used for training
        metadata: Additional metadata to save with the model
        
    Returns:
        Path to the saved model
    """
    logger = get_run_logger()
    
    # Create filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{dataset_name}_{model_name}_{timestamp}.joblib"
    output_path = MODEL_DIR / filename
    
    # Save the model
    logger.info(f"Saving model to {output_path}")
    joblib.dump(model, output_path)
    
    # Save metadata if provided
    if metadata:
        metadata_path = MODEL_DIR / f"{dataset_name}_{model_name}_{timestamp}_metadata.json"
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)
    
    # Create artifact
    create_markdown_artifact(
        markdown=f"## Model Saved\n\n"
                f"- **Model**: {model_name}\n"
                f"- **Dataset**: {dataset_name}\n"
                f"- **Path**: {output_path}\n"
                f"- **Timestamp**: {datetime.now().isoformat()}\n"
                f"- **Metadata**: {metadata}",
        key=f"model-save-{dataset_name}-{model_name}",
    )
    
    return output_path


@task
def load_model(model_path: Path) -> Any:
    """
    Load a trained model from disk.
    
    Args:
        model_path: Path to the saved model
        
    Returns:
        Loaded model
    """
    logger = get_run_logger()
    logger.info(f"Loading model from {model_path}")
    
    model = joblib.load(model_path)
    
    # Create artifact
    create_markdown_artifact(
        markdown=f"## Model Loaded\n\n"
                f"- **Path**: {model_path}\n"
                f"- **Timestamp**: {datetime.now().isoformat()}",
        key=f"model-load-{model_path.stem}",
    )
    
    return model


@task
def log_flow_run_info() -> Dict:
    """
    Log information about the current flow run.
    
    Returns:
        Dictionary with flow run information
    """
    context = get_run_context()
    logger = get_run_logger()
    
    flow_run_info = {
        "flow_name": context.flow_name,
        "flow_run_id": context.flow_run.id,
        "flow_run_name": context.flow_run.name,
        "flow_run_timestamp": datetime.now().isoformat(),
        "parameters": context.parameters,
    }
    
    logger.info(f"Flow run info: {flow_run_info}")
    
    # Create artifact
    create_markdown_artifact(
        markdown=f"## Flow Run Information\n\n"
                f"- **Flow Name**: {flow_run_info['flow_name']}\n"
                f"- **Flow Run ID**: {flow_run_info['flow_run_id']}\n"
                f"- **Flow Run Name**: {flow_run_info['flow_run_name']}\n"
                f"- **Timestamp**: {flow_run_info['flow_run_timestamp']}\n"
                f"- **Parameters**: {flow_run_info['parameters']}",
        key=f"flow-run-info-{context.flow_run.id}",
    )
    
    return flow_run_info 