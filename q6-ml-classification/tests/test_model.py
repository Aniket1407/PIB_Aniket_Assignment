import sys
from pathlib import Path
import numpy as np
import pandas as pd
import pytest

# Ensure q6 directory and src directory are accessible
q6_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(q6_dir))
sys.path.insert(0, str(q6_dir / "src"))

from src.train import (
    CATEGORICAL_FEATURES,
    NUMERICAL_FEATURES,
    TARGET_COLUMN,
    clean_dataset,
    evaluate_model,
    fit_preprocessors,
    load_dataset,
    split_data,
    split_features_target,
    train_model,
    transform_features,
)

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "churn_data.csv"


def test_1_dataset_contains_expected_columns():
    """Verify that the dataset contains all expected feature columns and target column."""
    df = load_dataset(DATA_PATH)
    expected_cols = set(NUMERICAL_FEATURES + CATEGORICAL_FEATURES + [TARGET_COLUMN])
    assert expected_cols.issubset(set(df.columns))
    assert len(df) > 0


def test_2_target_separated_correctly():
    """Verify that X contains only feature columns and y contains only the target variable."""
    df = load_dataset(DATA_PATH)
    df_clean = clean_dataset(df)
    X, y = split_features_target(df_clean)

    assert set(X.columns) == set(NUMERICAL_FEATURES + CATEGORICAL_FEATURES)
    assert TARGET_COLUMN not in X.columns
    assert len(y) == len(X)
    assert set(y.unique()).issubset({0, 1})


def test_3_train_test_split_works():
    """Verify train_test_split splits data with correct proportions and without leakage."""
    df = load_dataset(DATA_PATH)
    df_clean = clean_dataset(df)
    X, y = split_features_target(df_clean)

    X_train, X_test, y_train, y_test = split_data(X, y, test_size=0.2, random_state=42)

    assert len(X_train) == int(len(X) * 0.8)
    assert len(X_test) == int(len(X) * 0.2)
    assert len(y_train) == len(X_train)
    assert len(y_test) == len(X_test)


def test_4_preprocessing_can_be_fitted_on_training_data():
    """Verify numerical and categorical preprocessors fit on training data and transform features."""
    df = load_dataset(DATA_PATH)
    df_clean = clean_dataset(df)
    X, y = split_features_target(df_clean)
    X_train, X_test, y_train, y_test = split_data(X, y, test_size=0.2, random_state=42)

    preprocessors = fit_preprocessors(X_train)
    assert "num_imputer" in preprocessors
    assert "scaler" in preprocessors
    assert "cat_imputer" in preprocessors
    assert "encoder" in preprocessors

    X_train_proc = transform_features(preprocessors, X_train)
    X_test_proc = transform_features(preprocessors, X_test)

    assert isinstance(X_train_proc, np.ndarray)
    assert isinstance(X_test_proc, np.ndarray)
    assert X_train_proc.shape[0] == len(X_train)
    assert X_test_proc.shape[0] == len(X_test)
    assert X_train_proc.shape[1] == X_test_proc.shape[1]


def test_5_logistic_regression_can_be_trained():
    """Verify that the Logistic Regression model can be trained without errors."""
    df = load_dataset(DATA_PATH)
    df_clean = clean_dataset(df)
    X, y = split_features_target(df_clean)
    X_train, X_test, y_train, y_test = split_data(X, y, test_size=0.2, random_state=42)

    preprocessors = fit_preprocessors(X_train)
    X_train_proc = transform_features(preprocessors, X_train)

    model = train_model(X_train_proc, y_train, random_state=42)
    assert hasattr(model, "coef_")
    assert hasattr(model, "intercept_")
    assert hasattr(model, "classes_")


def test_6_predictions_are_generated():
    """Verify that the trained model generates predictions matching test sample count."""
    df = load_dataset(DATA_PATH)
    df_clean = clean_dataset(df)
    X, y = split_features_target(df_clean)
    X_train, X_test, y_train, y_test = split_data(X, y, test_size=0.2, random_state=42)

    preprocessors = fit_preprocessors(X_train)
    X_train_proc = transform_features(preprocessors, X_train)
    X_test_proc = transform_features(preprocessors, X_test)

    model = train_model(X_train_proc, y_train, random_state=42)
    preds = model.predict(X_test_proc)

    assert len(preds) == len(X_test)


def test_7_predictions_contain_valid_binary_values():
    """Verify that predictions contain only valid binary classes (0 or 1)."""
    df = load_dataset(DATA_PATH)
    df_clean = clean_dataset(df)
    X, y = split_features_target(df_clean)
    X_train, X_test, y_train, y_test = split_data(X, y, test_size=0.2, random_state=42)

    preprocessors = fit_preprocessors(X_train)
    X_train_proc = transform_features(preprocessors, X_train)
    X_test_proc = transform_features(preprocessors, X_test)

    model = train_model(X_train_proc, y_train, random_state=42)
    preds = model.predict(X_test_proc)

    unique_vals = set(np.unique(preds))
    assert unique_vals.issubset({0, 1})


def test_8_accuracy_can_be_calculated():
    """Verify that accuracy can be calculated and falls within a valid [0, 1] range."""
    df = load_dataset(DATA_PATH)
    df_clean = clean_dataset(df)
    X, y = split_features_target(df_clean)
    X_train, X_test, y_train, y_test = split_data(X, y, test_size=0.2, random_state=42)

    preprocessors = fit_preprocessors(X_train)
    X_train_proc = transform_features(preprocessors, X_train)
    X_test_proc = transform_features(preprocessors, X_test)

    model = train_model(X_train_proc, y_train, random_state=42)
    eval_metrics = evaluate_model(model, X_train_proc, y_train, X_test_proc, y_test)

    assert "test_accuracy" in eval_metrics
    assert 0.0 <= eval_metrics["test_accuracy"] <= 1.0
    assert "train_accuracy" in eval_metrics
    assert 0.0 <= eval_metrics["train_accuracy"] <= 1.0


def test_9_precision_can_be_calculated():
    """Verify that precision score is calculated as a valid float between 0 and 1."""
    df = load_dataset(DATA_PATH)
    df_clean = clean_dataset(df)
    X, y = split_features_target(df_clean)
    X_train, X_test, y_train, y_test = split_data(X, y, test_size=0.2, random_state=42)

    preprocessors = fit_preprocessors(X_train)
    X_train_proc = transform_features(preprocessors, X_train)
    X_test_proc = transform_features(preprocessors, X_test)

    model = train_model(X_train_proc, y_train, random_state=42)
    eval_metrics = evaluate_model(model, X_train_proc, y_train, X_test_proc, y_test)

    assert "test_precision" in eval_metrics
    assert 0.0 <= eval_metrics["test_precision"] <= 1.0


def test_10_recall_can_be_calculated():
    """Verify that recall score is calculated as a valid float between 0 and 1."""
    df = load_dataset(DATA_PATH)
    df_clean = clean_dataset(df)
    X, y = split_features_target(df_clean)
    X_train, X_test, y_train, y_test = split_data(X, y, test_size=0.2, random_state=42)

    preprocessors = fit_preprocessors(X_train)
    X_train_proc = transform_features(preprocessors, X_train)
    X_test_proc = transform_features(preprocessors, X_test)

    model = train_model(X_train_proc, y_train, random_state=42)
    eval_metrics = evaluate_model(model, X_train_proc, y_train, X_test_proc, y_test)

    assert "test_recall" in eval_metrics
    assert 0.0 <= eval_metrics["test_recall"] <= 1.0


def test_11_missing_feature_values_handled_by_preprocessing():
    """Verify that missing values in numerical and categorical features are handled safely by imputers."""
    df = load_dataset(DATA_PATH)
    df_clean = clean_dataset(df)
    X, y = split_features_target(df_clean)
    X_train, X_test, y_train, y_test = split_data(X, y, test_size=0.2, random_state=42)

    preprocessors = fit_preprocessors(X_train)

    # Construct input with missing values in both numerical and categorical columns
    corrupted_sample = pd.DataFrame(
        [
            {
                "Age": np.nan,
                "income": 50000,
                "number_of_logins": np.nan,
                "purchase_count": 3,
                "last_login_days": 10,
                "subscription": np.nan,
            }
        ]
    )

    transformed = transform_features(preprocessors, corrupted_sample)
    assert not np.isnan(transformed).any()
    assert transformed.shape[1] == len(NUMERICAL_FEATURES) + len(
        preprocessors["encoder"].get_feature_names_out(CATEGORICAL_FEATURES)
    )
