"""
Visualization flows for the Streamlit portfolio.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Tuple
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
import base64
import json
import os
from datetime import datetime

from prefect import flow, task, get_run_logger
from prefect.artifacts import create_markdown_artifact
from prefect.tasks import task_input_hash
from datetime import timedelta

from .config import VISUALIZATION_FLOW, DATASETS
from .utils import (
    load_dataset,
    log_flow_run_info,
)


@task
def load_data_for_visualization(
    dataset_name: str,
    dataset_path: Optional[Path] = None,
    dataset_type: str = "processed",
) -> pd.DataFrame:
    """
    Load data for visualization.
    
    Args:
        dataset_name: Name of the dataset
        dataset_path: Path to the dataset file (if None, uses default path)
        dataset_type: Type of dataset (raw, processed, train, test, val)
        
    Returns:
        DataFrame with loaded data
    """
    logger = get_run_logger()
    
    if dataset_path is None:
        if dataset_type == "raw":
            dataset_path = Path(f"data/raw/{DATASETS[dataset_name]['filename']}")
        else:
            dataset_path = Path(f"data/processed/{dataset_name}_{dataset_type}.csv")
    
    logger.info(f"Loading {dataset_name} data from {dataset_path}")
    
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset file not found: {dataset_path}")
    
    # Load the dataset
    df = pd.read_csv(dataset_path)
    
    logger.info(f"Loaded data with shape: {df.shape}")
    
    return df


@task
def create_exploratory_visualizations(
    df: pd.DataFrame,
    dataset_name: str,
    output_dir: Path = Path("assets/images/visualizations"),
) -> List[Dict]:
    """
    Create exploratory visualizations for a dataset.
    
    Args:
        df: DataFrame to visualize
        dataset_name: Name of the dataset
        output_dir: Directory to save visualizations
        
    Returns:
        List of dictionaries with visualization metadata
    """
    logger = get_run_logger()
    logger.info(f"Creating exploratory visualizations for {dataset_name}")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # List to store visualization metadata
    visualizations = []
    
    # Get numeric and categorical columns
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    
    logger.info(f"Numeric columns: {len(numeric_cols)}")
    logger.info(f"Categorical columns: {len(categorical_cols)}")
    
    # 1. Distribution of numeric features
    if numeric_cols:
        logger.info("Creating distribution plots for numeric features")
        
        # Create a subplot for each numeric column
        n_cols = min(3, len(numeric_cols))
        n_rows = (len(numeric_cols) + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, n_rows * 4))
        fig.suptitle(f"Distribution of Numeric Features - {dataset_name}", fontsize=16)
        
        for i, col in enumerate(numeric_cols):
            row, col_idx = i // n_cols, i % n_cols
            ax = axes[row, col_idx] if n_rows > 1 else axes[col_idx]
            
            # Histogram with KDE
            sns.histplot(df[col].dropna(), kde=True, ax=ax)
            ax.set_title(f"Distribution of {col}")
            ax.set_xlabel(col)
            ax.set_ylabel("Frequency")
        
        # Hide empty subplots
        for i in range(len(numeric_cols), n_rows * n_cols):
            row, col_idx = i // n_cols, i % n_cols
            ax = axes[row, col_idx] if n_rows > 1 else axes[col_idx]
            ax.axis("off")
        
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        
        # Save the figure
        output_path = output_dir / f"{dataset_name}_numeric_distributions.png"
        plt.savefig(output_path)
        plt.close()
        
        # Add to visualizations list
        visualizations.append({
            "title": "Distribution of Numeric Features",
            "description": "Histograms with KDE for numeric features",
            "path": str(output_path),
            "type": "distribution",
            "features": numeric_cols
        })
    
    # 2. Correlation heatmap for numeric features
    if len(numeric_cols) > 1:
        logger.info("Creating correlation heatmap")
        
        plt.figure(figsize=(12, 10))
        corr = df[numeric_cols].corr()
        mask = np.triu(np.ones_like(corr, dtype=bool))
        sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="coolwarm", 
                   square=True, linewidths=0.5, cbar_kws={"shrink": 0.8})
        plt.title(f"Correlation Heatmap - {dataset_name}", fontsize=16)
        plt.tight_layout()
        
        # Save the figure
        output_path = output_dir / f"{dataset_name}_correlation_heatmap.png"
        plt.savefig(output_path)
        plt.close()
        
        # Add to visualizations list
        visualizations.append({
            "title": "Correlation Heatmap",
            "description": "Heatmap showing correlations between numeric features",
            "path": str(output_path),
            "type": "correlation",
            "features": numeric_cols
        })
    
    # 3. Count plots for categorical features
    if categorical_cols:
        logger.info("Creating count plots for categorical features")
        
        # Create a subplot for each categorical column
        n_cols = min(2, len(categorical_cols))
        n_rows = (len(categorical_cols) + n_cols - 1) // n_cols
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, n_rows * 5))
        fig.suptitle(f"Distribution of Categorical Features - {dataset_name}", fontsize=16)
        
        for i, col in enumerate(categorical_cols):
            row, col_idx = i // n_cols, i % n_cols
            ax = axes[row, col_idx] if n_rows > 1 and n_cols > 1 else axes[i] if n_rows > 1 or n_cols > 1 else axes
            
            # Count plot
            value_counts = df[col].value_counts().sort_values(ascending=False)
            
            # If too many categories, limit to top 10
            if len(value_counts) > 10:
                value_counts = value_counts.head(10)
                ax.set_title(f"Top 10 Categories for {col}")
            else:
                ax.set_title(f"Categories for {col}")
            
            sns.barplot(x=value_counts.index, y=value_counts.values, ax=ax)
            ax.set_xlabel(col)
            ax.set_ylabel("Count")
            ax.tick_params(axis='x', rotation=45)
        
        # Hide empty subplots
        if len(categorical_cols) < n_rows * n_cols:
            for i in range(len(categorical_cols), n_rows * n_cols):
                row, col_idx = i // n_cols, i % n_cols
                ax = axes[row, col_idx] if n_rows > 1 and n_cols > 1 else axes[i] if n_rows > 1 or n_cols > 1 else axes
                ax.axis("off")
        
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        
        # Save the figure
        output_path = output_dir / f"{dataset_name}_categorical_distributions.png"
        plt.savefig(output_path)
        plt.close()
        
        # Add to visualizations list
        visualizations.append({
            "title": "Distribution of Categorical Features",
            "description": "Count plots for categorical features",
            "path": str(output_path),
            "type": "categorical",
            "features": categorical_cols
        })
    
    # 4. Pair plot for selected numeric features
    if len(numeric_cols) >= 2:
        logger.info("Creating pair plot")
        
        # Select a subset of numeric columns if there are too many
        selected_numeric_cols = numeric_cols[:5] if len(numeric_cols) > 5 else numeric_cols
        
        # Add a categorical column for hue if available
        hue_col = None
        if categorical_cols and df[categorical_cols[0]].nunique() <= 10:
            hue_col = categorical_cols[0]
        
        # Create pair plot
        plt.figure(figsize=(12, 10))
        pair_plot = sns.pairplot(df[selected_numeric_cols + ([hue_col] if hue_col else [])], 
                               hue=hue_col, height=2.5, aspect=1.2, 
                               plot_kws={"alpha": 0.7})
        pair_plot.fig.suptitle(f"Pair Plot - {dataset_name}", y=1.02, fontsize=16)
        
        # Save the figure
        output_path = output_dir / f"{dataset_name}_pair_plot.png"
        plt.savefig(output_path)
        plt.close()
        
        # Add to visualizations list
        visualizations.append({
            "title": "Pair Plot",
            "description": "Scatter plots and distributions for selected numeric features",
            "path": str(output_path),
            "type": "pairplot",
            "features": selected_numeric_cols + ([hue_col] if hue_col else [])
        })
    
    # 5. Box plots for numeric features by a categorical feature
    if numeric_cols and categorical_cols:
        logger.info("Creating box plots")
        
        # Find a suitable categorical column (not too many categories)
        cat_col = None
        for col in categorical_cols:
            if df[col].nunique() <= 5:
                cat_col = col
                break
        
        if cat_col:
            # Select a subset of numeric columns if there are too many
            selected_numeric_cols = numeric_cols[:6] if len(numeric_cols) > 6 else numeric_cols
            
            # Create a subplot for each numeric column
            n_cols = min(3, len(selected_numeric_cols))
            n_rows = (len(selected_numeric_cols) + n_cols - 1) // n_cols
            
            fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, n_rows * 5))
            fig.suptitle(f"Box Plots by {cat_col} - {dataset_name}", fontsize=16)
            
            for i, num_col in enumerate(selected_numeric_cols):
                row, col_idx = i // n_cols, i % n_cols
                ax = axes[row, col_idx] if n_rows > 1 and n_cols > 1 else axes[i] if n_rows > 1 or n_cols > 1 else axes
                
                # Box plot
                sns.boxplot(x=cat_col, y=num_col, data=df, ax=ax)
                ax.set_title(f"{num_col} by {cat_col}")
                ax.set_xlabel(cat_col)
                ax.set_ylabel(num_col)
                ax.tick_params(axis='x', rotation=45)
            
            # Hide empty subplots
            if len(selected_numeric_cols) < n_rows * n_cols:
                for i in range(len(selected_numeric_cols), n_rows * n_cols):
                    row, col_idx = i // n_cols, i % n_cols
                    ax = axes[row, col_idx] if n_rows > 1 and n_cols > 1 else axes[i] if n_rows > 1 or n_cols > 1 else axes
                    ax.axis("off")
            
            plt.tight_layout(rect=[0, 0, 1, 0.96])
            
            # Save the figure
            output_path = output_dir / f"{dataset_name}_box_plots.png"
            plt.savefig(output_path)
            plt.close()
            
            # Add to visualizations list
            visualizations.append({
                "title": f"Box Plots by {cat_col}",
                "description": f"Box plots showing distribution of numeric features by {cat_col}",
                "path": str(output_path),
                "type": "boxplot",
                "features": selected_numeric_cols,
                "category": cat_col
            })
    
    # Save visualization metadata
    metadata_path = output_dir / f"{dataset_name}_visualizations.json"
    with open(metadata_path, "w") as f:
        json.dump(visualizations, f, indent=2)
    
    # Create artifact with visualizations
    visualization_md = "\n\n".join([
        f"### {viz['title']}\n"
        f"{viz['description']}\n"
        f"![{viz['title']}]({viz['path']})"
        for viz in visualizations
    ])
    
    create_markdown_artifact(
        markdown=f"## Exploratory Visualizations for {dataset_name}\n\n"
                f"Created {len(visualizations)} visualizations.\n\n"
                f"{visualization_md}",
        key=f"visualizations-{dataset_name}",
    )
    
    return visualizations


@task
def create_interactive_visualizations(
    df: pd.DataFrame,
    dataset_name: str,
    output_dir: Path = Path("assets/images/interactive"),
) -> List[Dict]:
    """
    Create interactive visualizations using Plotly.
    
    Args:
        df: DataFrame to visualize
        dataset_name: Name of the dataset
        output_dir: Directory to save visualizations
        
    Returns:
        List of dictionaries with visualization metadata
    """
    logger = get_run_logger()
    logger.info(f"Creating interactive visualizations for {dataset_name}")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # List to store visualization metadata
    visualizations = []
    
    # Get numeric and categorical columns
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
    
    # 1. Interactive scatter plot matrix
    if len(numeric_cols) >= 2:
        logger.info("Creating interactive scatter plot matrix")
        
        # Select a subset of numeric columns if there are too many
        selected_numeric_cols = numeric_cols[:4] if len(numeric_cols) > 4 else numeric_cols
        
        # Add a categorical column for color if available
        color_col = None
        if categorical_cols and df[categorical_cols[0]].nunique() <= 10:
            color_col = categorical_cols[0]
        
        # Create scatter plot matrix
        fig = px.scatter_matrix(
            df,
            dimensions=selected_numeric_cols,
            color=color_col,
            title=f"Scatter Plot Matrix - {dataset_name}",
            opacity=0.7,
        )
        
        # Update layout
        fig.update_layout(
            title_font_size=16,
            width=900,
            height=900,
        )
        
        # Save as HTML
        output_path = output_dir / f"{dataset_name}_scatter_matrix.html"
        fig.write_html(output_path)
        
        # Add to visualizations list
        visualizations.append({
            "title": "Interactive Scatter Plot Matrix",
            "description": "Matrix of scatter plots for selected numeric features",
            "path": str(output_path),
            "type": "scatter_matrix",
            "features": selected_numeric_cols,
            "color": color_col
        })
    
    # 2. Interactive bar chart for categorical features
    if categorical_cols:
        logger.info("Creating interactive bar chart")
        
        # Select a categorical column
        cat_col = categorical_cols[0]
        
        # Count values
        value_counts = df[cat_col].value_counts().reset_index()
        value_counts.columns = [cat_col, "count"]
        
        # Create bar chart
        fig = px.bar(
            value_counts,
            x=cat_col,
            y="count",
            title=f"Distribution of {cat_col} - {dataset_name}",
            color="count",
            color_continuous_scale="Viridis",
        )
        
        # Update layout
        fig.update_layout(
            title_font_size=16,
            xaxis_title=cat_col,
            yaxis_title="Count",
            width=800,
            height=500,
        )
        
        # Save as HTML
        output_path = output_dir / f"{dataset_name}_{cat_col}_bar_chart.html"
        fig.write_html(output_path)
        
        # Add to visualizations list
        visualizations.append({
            "title": f"Interactive Bar Chart for {cat_col}",
            "description": f"Bar chart showing the distribution of {cat_col}",
            "path": str(output_path),
            "type": "bar_chart",
            "features": [cat_col]
        })
    
    # 3. Interactive heatmap for correlations
    if len(numeric_cols) > 1:
        logger.info("Creating interactive correlation heatmap")
        
        # Calculate correlation matrix
        corr = df[numeric_cols].corr()
        
        # Create heatmap
        fig = px.imshow(
            corr,
            text_auto=".2f",
            aspect="auto",
            color_continuous_scale="RdBu_r",
            title=f"Correlation Heatmap - {dataset_name}",
        )
        
        # Update layout
        fig.update_layout(
            title_font_size=16,
            width=800,
            height=800,
        )
        
        # Save as HTML
        output_path = output_dir / f"{dataset_name}_correlation_heatmap.html"
        fig.write_html(output_path)
        
        # Add to visualizations list
        visualizations.append({
            "title": "Interactive Correlation Heatmap",
            "description": "Heatmap showing correlations between numeric features",
            "path": str(output_path),
            "type": "correlation_heatmap",
            "features": numeric_cols
        })
    
    # 4. Interactive histogram for numeric features
    if numeric_cols:
        logger.info("Creating interactive histograms")
        
        # Create subplots
        fig = make_subplots(
            rows=len(numeric_cols),
            cols=1,
            subplot_titles=[f"Distribution of {col}" for col in numeric_cols],
            vertical_spacing=0.05,
        )
        
        # Add histograms
        for i, col in enumerate(numeric_cols):
            fig.add_trace(
                go.Histogram(
                    x=df[col],
                    name=col,
                    marker_color=px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)],
                ),
                row=i+1,
                col=1,
            )
        
        # Update layout
        fig.update_layout(
            title_text=f"Distributions of Numeric Features - {dataset_name}",
            title_font_size=16,
            showlegend=False,
            height=300 * len(numeric_cols),
            width=800,
        )
        
        # Save as HTML
        output_path = output_dir / f"{dataset_name}_histograms.html"
        fig.write_html(output_path)
        
        # Add to visualizations list
        visualizations.append({
            "title": "Interactive Histograms",
            "description": "Histograms showing distributions of numeric features",
            "path": str(output_path),
            "type": "histograms",
            "features": numeric_cols
        })
    
    # 5. Interactive 3D scatter plot (if at least 3 numeric columns)
    if len(numeric_cols) >= 3:
        logger.info("Creating interactive 3D scatter plot")
        
        # Select 3 numeric columns
        x_col, y_col, z_col = numeric_cols[:3]
        
        # Add a categorical column for color if available
        color_col = None
        if categorical_cols and df[categorical_cols[0]].nunique() <= 10:
            color_col = categorical_cols[0]
        
        # Create 3D scatter plot
        fig = px.scatter_3d(
            df,
            x=x_col,
            y=y_col,
            z=z_col,
            color=color_col,
            title=f"3D Scatter Plot - {dataset_name}",
            opacity=0.7,
        )
        
        # Update layout
        fig.update_layout(
            title_font_size=16,
            width=900,
            height=700,
        )
        
        # Save as HTML
        output_path = output_dir / f"{dataset_name}_3d_scatter.html"
        fig.write_html(output_path)
        
        # Add to visualizations list
        visualizations.append({
            "title": "Interactive 3D Scatter Plot",
            "description": f"3D scatter plot of {x_col}, {y_col}, and {z_col}",
            "path": str(output_path),
            "type": "3d_scatter",
            "features": [x_col, y_col, z_col],
            "color": color_col
        })
    
    # Save visualization metadata
    metadata_path = output_dir / f"{dataset_name}_interactive_visualizations.json"
    with open(metadata_path, "w") as f:
        json.dump(visualizations, f, indent=2)
    
    # Create artifact with visualizations
    visualization_md = "\n\n".join([
        f"### {viz['title']}\n"
        f"{viz['description']}\n"
        f"[View Interactive Visualization]({viz['path']})"
        for viz in visualizations
    ])
    
    create_markdown_artifact(
        markdown=f"## Interactive Visualizations for {dataset_name}\n\n"
                f"Created {len(visualizations)} interactive visualizations.\n\n"
                f"{visualization_md}",
        key=f"interactive-visualizations-{dataset_name}",
    )
    
    return visualizations


@flow(
    name=VISUALIZATION_FLOW.name,
    description=VISUALIZATION_FLOW.description,
    retries=VISUALIZATION_FLOW.retries,
    retry_delay_seconds=VISUALIZATION_FLOW.retry_delay_seconds,
    log_prints=VISUALIZATION_FLOW.log_prints,
)
def generate_visualizations(
    dataset_name: str,
    dataset_path: Optional[Path] = None,
    dataset_type: str = "processed",
    create_static: bool = True,
    create_interactive: bool = True,
    output_dir: Path = Path("assets/images"),
) -> Dict[str, List[Dict]]:
    """
    Generate visualizations for a dataset.
    
    Args:
        dataset_name: Name of the dataset
        dataset_path: Path to the dataset file (if None, uses default path)
        dataset_type: Type of dataset (raw, processed, train, test, val)
        create_static: Whether to create static visualizations
        create_interactive: Whether to create interactive visualizations
        output_dir: Base directory to save visualizations
        
    Returns:
        Dictionary with visualization metadata
    """
    # Log flow run info
    log_flow_run_info()
    
    # Load data
    df = load_data_for_visualization(
        dataset_name=dataset_name,
        dataset_path=dataset_path,
        dataset_type=dataset_type,
    )
    
    results = {}
    
    # Create static visualizations
    if create_static:
        static_output_dir = output_dir / "visualizations"
        static_visualizations = create_exploratory_visualizations(
            df=df,
            dataset_name=dataset_name,
            output_dir=static_output_dir,
        )
        results["static"] = static_visualizations
    
    # Create interactive visualizations
    if create_interactive:
        interactive_output_dir = output_dir / "interactive"
        interactive_visualizations = create_interactive_visualizations(
            df=df,
            dataset_name=dataset_name,
            output_dir=interactive_output_dir,
        )
        results["interactive"] = interactive_visualizations
    
    # Create summary artifact
    create_markdown_artifact(
        markdown=f"## Visualization Generation Summary for {dataset_name}\n\n"
                f"- **Dataset**: {dataset_name}\n"
                f"- **Dataset Type**: {dataset_type}\n"
                f"- **Dataset Shape**: {df.shape}\n"
                f"- **Static Visualizations**: {len(results.get('static', []))}\n"
                f"- **Interactive Visualizations**: {len(results.get('interactive', []))}\n"
                f"- **Output Directory**: {output_dir}\n"
                f"- **Timestamp**: {datetime.now().isoformat()}",
        key=f"visualization-summary-{dataset_name}",
    )
    
    return results


if __name__ == "__main__":
    # Example usage
    generate_visualizations("customer_churn") 