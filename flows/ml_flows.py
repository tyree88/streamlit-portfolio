"""
Machine learning flows for the Streamlit portfolio.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Tuple
import json
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score,
    mean_squared_error, mean_absolute_error, r2_score, confusion_matrix,
    classification_report
)

# ML models
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

from prefect import flow, task, get_run_logger
from prefect.artifacts import create_markdown_artifact
from prefect.tasks import task_input_hash
from datetime import timedelta
import io
import base64

from .config import ML_TRAINING_FLOW, ML_EVALUATION_FLOW, DATASETS, MODELS
from .utils import (
    load_dataset,
    save_model,
    load_model,
    log_flow_run_info,
)


@task
def prepare_features_and_target(
    df: pd.DataFrame,
    dataset_name: str,
) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Prepare features and target for model training.
    
    Args:
        df: DataFrame with features and target
        dataset_name: Name of the dataset
        
    Returns:
        Tuple of features DataFrame and target Series
    """
    logger = get_run_logger()
    logger.info(f"Preparing features and target for {dataset_name}")
    
    # Get target variable
    target = DATASETS[dataset_name]["target"]
    
    if target not in df.columns:
        raise ValueError(f"Target column '{target}' not found in dataset")
    
    # Split features and target
    X = df.drop(columns=[target])
    y = df[target]
    
    logger.info(f"Features shape: {X.shape}")
    logger.info(f"Target shape: {y.shape}")
    
    return X, y


@task
def create_preprocessing_pipeline(
    X: pd.DataFrame,
    dataset_name: str,
) -> ColumnTransformer:
    """
    Create a preprocessing pipeline for the features.
    
    Args:
        X: Features DataFrame
        dataset_name: Name of the dataset
        
    Returns:
        Preprocessing pipeline
    """
    logger = get_run_logger()
    logger.info(f"Creating preprocessing pipeline for {dataset_name}")
    
    # Identify numeric and categorical columns
    numeric_cols = X.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols = X.select_dtypes(include=["object", "category"]).columns.tolist()
    
    logger.info(f"Numeric columns: {len(numeric_cols)}")
    logger.info(f"Categorical columns: {len(categorical_cols)}")
    
    # Create preprocessing pipelines
    numeric_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])
    
    categorical_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])
    
    # Combine preprocessing steps
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_cols),
            ("cat", categorical_transformer, categorical_cols)
        ]
    )
    
    return preprocessor


@task
def train_model_task(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    preprocessor: ColumnTransformer,
    algorithm: str,
    dataset_name: str,
    hyperparams: Dict = None,
) -> Tuple[Any, Dict]:
    """
    Train a machine learning model.
    
    Args:
        X_train: Training features
        y_train: Training target
        preprocessor: Preprocessing pipeline
        algorithm: Algorithm to use
        dataset_name: Name of the dataset
        hyperparams: Hyperparameters for the model
        
    Returns:
        Tuple of trained model and training metadata
    """
    logger = get_run_logger()
    logger.info(f"Training {algorithm} model for {dataset_name}")
    
    # Default hyperparameters
    default_hyperparams = {
        "random_forest": {
            "n_estimators": 100,
            "max_depth": None,
            "min_samples_split": 2,
            "random_state": 42
        },
        "gradient_boosting": {
            "n_estimators": 100,
            "learning_rate": 0.1,
            "max_depth": 3,
            "random_state": 42
        },
        "logistic_regression": {
            "C": 1.0,
            "max_iter": 1000,
            "random_state": 42
        },
        "linear_regression": {},
        "svm": {
            "C": 1.0,
            "kernel": "rbf",
            "random_state": 42
        },
        "knn": {
            "n_neighbors": 5,
            "weights": "uniform"
        }
    }
    
    # Use provided hyperparameters or defaults
    params = hyperparams or default_hyperparams.get(algorithm, {})
    
    # Create model based on algorithm
    problem_type = "classification" if y_train.dtype == "object" or y_train.nunique() <= 5 else "regression"
    
    if algorithm == "random_forest":
        if problem_type == "classification":
            model = RandomForestClassifier(**params)
        else:
            model = RandomForestRegressor(**params)
    
    elif algorithm == "gradient_boosting":
        if problem_type == "classification":
            model = GradientBoostingClassifier(**params)
        else:
            model = GradientBoostingRegressor(**params)
    
    elif algorithm == "logistic_regression":
        if problem_type != "classification":
            logger.warning("Logistic regression is for classification. Using linear regression instead.")
            model = LinearRegression()
        else:
            model = LogisticRegression(**params)
    
    elif algorithm == "linear_regression":
        if problem_type != "regression":
            logger.warning("Linear regression is for regression. Using logistic regression instead.")
            model = LogisticRegression()
        else:
            model = LinearRegression(**params)
    
    elif algorithm == "svm":
        model = SVC(**params, probability=True)
    
    elif algorithm == "knn":
        model = KNeighborsClassifier(**params)
    
    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")
    
    # Create pipeline with preprocessing
    pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ])
    
    # Train the model
    logger.info(f"Fitting {algorithm} model")
    pipeline.fit(X_train, y_train)
    
    # Cross-validation
    cv_folds = MODELS[dataset_name].get("cv_folds", 5)
    
    if problem_type == "classification":
        cv_scores = cross_val_score(pipeline, X_train, y_train, cv=cv_folds, scoring="accuracy")
    else:
        cv_scores = cross_val_score(pipeline, X_train, y_train, cv=cv_folds, scoring="neg_mean_squared_error")
    
    # Training metadata
    metadata = {
        "algorithm": algorithm,
        "dataset": dataset_name,
        "problem_type": problem_type,
        "hyperparameters": params,
        "cv_folds": cv_folds,
        "cv_scores": cv_scores.tolist(),
        "cv_score_mean": cv_scores.mean(),
        "cv_score_std": cv_scores.std(),
        "feature_count": X_train.shape[1],
        "training_samples": X_train.shape[0],
    }
    
    logger.info(f"Model training complete. CV score: {metadata['cv_score_mean']:.4f} ± {metadata['cv_score_std']:.4f}")
    
    # Create artifact
    create_markdown_artifact(
        markdown=f"## Model Training: {algorithm} for {dataset_name}\n\n"
                f"- **Algorithm**: {algorithm}\n"
                f"- **Problem Type**: {problem_type}\n"
                f"- **Features**: {X_train.shape[1]}\n"
                f"- **Training Samples**: {X_train.shape[0]}\n"
                f"- **CV Score**: {metadata['cv_score_mean']:.4f} ± {metadata['cv_score_std']:.4f}\n"
                f"- **Hyperparameters**: {params}",
        key=f"model-training-{dataset_name}-{algorithm}",
    )
    
    return pipeline, metadata


@task
def evaluate_model_task(
    model: Any,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    dataset_name: str,
    algorithm: str,
) -> Dict:
    """
    Evaluate a trained model on test data.
    
    Args:
        model: Trained model
        X_test: Test features
        y_test: Test target
        dataset_name: Name of the dataset
        algorithm: Algorithm used
        
    Returns:
        Dictionary with evaluation metrics
    """
    logger = get_run_logger()
    logger.info(f"Evaluating {algorithm} model for {dataset_name}")
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Determine problem type
    problem_type = "classification" if y_test.dtype == "object" or y_test.nunique() <= 5 else "regression"
    
    # Calculate metrics
    metrics = {}
    
    if problem_type == "classification":
        # Classification metrics
        metrics["accuracy"] = accuracy_score(y_test, y_pred)
        
        # For binary classification
        if y_test.nunique() == 2:
            metrics["precision"] = precision_score(y_test, y_pred, average="binary")
            metrics["recall"] = recall_score(y_test, y_pred, average="binary")
            metrics["f1"] = f1_score(y_test, y_pred, average="binary")
            
            # ROC AUC (requires probability predictions)
            try:
                y_prob = model.predict_proba(X_test)[:, 1]
                metrics["roc_auc"] = roc_auc_score(y_test, y_prob)
            except:
                logger.warning("Could not calculate ROC AUC score")
        
        # For multiclass classification
        else:
            metrics["precision"] = precision_score(y_test, y_pred, average="weighted")
            metrics["recall"] = recall_score(y_test, y_pred, average="weighted")
            metrics["f1"] = f1_score(y_test, y_pred, average="weighted")
        
        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        metrics["confusion_matrix"] = cm.tolist()
        
        # Classification report
        report = classification_report(y_test, y_pred, output_dict=True)
        metrics["classification_report"] = report
        
    else:
        # Regression metrics
        metrics["rmse"] = np.sqrt(mean_squared_error(y_test, y_pred))
        metrics["mae"] = mean_absolute_error(y_test, y_pred)
        metrics["r2"] = r2_score(y_test, y_pred)
    
    logger.info(f"Evaluation complete: {metrics}")
    
    # Create visualization
    plt.figure(figsize=(10, 6))
    
    if problem_type == "classification":
        # Plot confusion matrix
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", 
                    xticklabels=np.unique(y_test),
                    yticklabels=np.unique(y_test))
        plt.xlabel("Predicted")
        plt.ylabel("True")
        plt.title(f"Confusion Matrix - {algorithm} for {dataset_name}")
    else:
        # Plot predicted vs actual
        plt.scatter(y_test, y_pred, alpha=0.5)
        plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--')
        plt.xlabel("Actual")
        plt.ylabel("Predicted")
        plt.title(f"Predicted vs Actual - {algorithm} for {dataset_name}")
    
    # Save plot to buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    
    # Convert plot to base64 for artifact
    plot_data = base64.b64encode(buf.read()).decode("utf-8")
    
    # Create artifact with metrics and plot
    metrics_md = "\n".join([f"- **{k}**: {v:.4f}" if isinstance(v, float) else f"- **{k}**: {v}" 
                           for k, v in metrics.items() if not isinstance(v, (list, dict))])
    
    create_markdown_artifact(
        markdown=f"## Model Evaluation: {algorithm} for {dataset_name}\n\n"
                f"{metrics_md}\n\n"
                f"![Evaluation Plot](data:image/png;base64,{plot_data})",
        key=f"model-evaluation-{dataset_name}-{algorithm}",
    )
    
    return metrics


@flow(
    name=ML_TRAINING_FLOW.name,
    description=ML_TRAINING_FLOW.description,
    retries=ML_TRAINING_FLOW.retries,
    retry_delay_seconds=ML_TRAINING_FLOW.retry_delay_seconds,
    log_prints=ML_TRAINING_FLOW.log_prints,
)
def train_model(
    dataset_name: str,
    algorithm: str = None,
    train_path: Path = None,
    hyperparams: Dict = None,
) -> Tuple[Path, Dict]:
    """
    Train a machine learning model on a processed dataset.
    
    Args:
        dataset_name: Name of the dataset
        algorithm: Algorithm to use (if None, uses all configured algorithms)
        train_path: Path to the training dataset (if None, uses default path)
        hyperparams: Hyperparameters for the model
        
    Returns:
        Tuple of path to the saved model and training metadata
    """
    # Log flow run info
    log_flow_run_info()
    
    # Determine algorithms to use
    algorithms = [algorithm] if algorithm else MODELS[dataset_name]["algorithms"]
    
    # Load training data
    if train_path is None:
        train_path = Path(f"data/processed/{dataset_name}_train.csv")
    
    train_df = pd.read_csv(train_path)
    
    # Prepare features and target
    X_train, y_train = prepare_features_and_target(train_df, dataset_name)
    
    # Create preprocessing pipeline
    preprocessor = create_preprocessing_pipeline(X_train, dataset_name)
    
    # Train models
    results = []
    for alg in algorithms:
        model, metadata = train_model_task(X_train, y_train, preprocessor, alg, dataset_name, hyperparams)
        
        # Save model
        model_path = save_model(model, alg, dataset_name, metadata)
        
        results.append((model_path, metadata))
    
    # Return the best model based on CV score
    best_model_idx = np.argmax([metadata["cv_score_mean"] for _, metadata in results])
    return results[best_model_idx]


@flow(
    name=ML_EVALUATION_FLOW.name,
    description=ML_EVALUATION_FLOW.description,
    retries=ML_EVALUATION_FLOW.retries,
    retry_delay_seconds=ML_EVALUATION_FLOW.retry_delay_seconds,
    log_prints=ML_EVALUATION_FLOW.log_prints,
)
def evaluate_model(
    dataset_name: str,
    model_path: Path = None,
    test_path: Path = None,
) -> Dict:
    """
    Evaluate a trained model on test data.
    
    Args:
        dataset_name: Name of the dataset
        model_path: Path to the trained model (if None, uses the latest model)
        test_path: Path to the test dataset (if None, uses default path)
        
    Returns:
        Dictionary with evaluation metrics
    """
    # Log flow run info
    log_flow_run_info()
    
    # Find the latest model if not specified
    if model_path is None:
        model_dir = Path("models")
        model_files = list(model_dir.glob(f"{dataset_name}_*.joblib"))
        if not model_files:
            raise ValueError(f"No models found for dataset {dataset_name}")
        
        # Sort by modification time (newest first)
        model_path = sorted(model_files, key=lambda p: p.stat().st_mtime, reverse=True)[0]
    
    # Load the model
    model = load_model(model_path)
    
    # Extract algorithm from model path
    algorithm = model_path.stem.split("_")[1]
    
    # Load test data
    if test_path is None:
        test_path = Path(f"data/processed/{dataset_name}_test.csv")
    
    test_df = pd.read_csv(test_path)
    
    # Prepare features and target
    X_test, y_test = prepare_features_and_target(test_df, dataset_name)
    
    # Evaluate model
    metrics = evaluate_model_task(model, X_test, y_test, dataset_name, algorithm)
    
    return metrics


if __name__ == "__main__":
    # Example usage
    model_path, metadata = train_model("customer_churn", algorithm="random_forest")
    metrics = evaluate_model("customer_churn", model_path=model_path) 