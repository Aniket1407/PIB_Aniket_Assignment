import sys
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler

NUMERICAL_FEATURES = [
    "Age",
    "income",
    "number_of_logins",
    "purchase_count",
    "last_login_days",
]
CATEGORICAL_FEATURES = ["subscription"]
TARGET_COLUMN = "will_churn"
ALL_COLUMNS = NUMERICAL_FEATURES + CATEGORICAL_FEATURES + [TARGET_COLUMN]


def load_dataset(file_path):
    """
    Stage 1: Load the CSV dataset.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset file not found: {file_path}")
    return pd.read_csv(path)


def clean_dataset(df):
    """
    Stage 2: Validate columns, drop exact duplicates,
    and normalize target column values (supports 0/1, Yes/No, true/false).
    """
    expected = set(ALL_COLUMNS)
    missing = expected - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns in dataset: {missing}")

    df_clean = df.drop_duplicates().reset_index(drop=True).copy()

    # Standardize target if encoded as strings
    if df_clean[TARGET_COLUMN].dtype == object:
        mapping = {
            "yes": 1,
            "no": 0,
            "1": 1,
            "0": 0,
            "true": 1,
            "false": 0,
        }
        df_clean[TARGET_COLUMN] = (
            df_clean[TARGET_COLUMN]
            .astype(str)
            .str.strip()
            .str.lower()
            .map(mapping)
        )
        if df_clean[TARGET_COLUMN].isnull().any():
            raise ValueError("Target column contains unrecognized non-binary values.")

    df_clean[TARGET_COLUMN] = df_clean[TARGET_COLUMN].astype(int)
    return df_clean


def split_features_target(df):
    """
    Stage 3: Separate feature matrix X and target vector y.
    """
    X = df[NUMERICAL_FEATURES + CATEGORICAL_FEATURES].copy()
    y = df[TARGET_COLUMN].copy()
    return X, y


def split_data(X, y, test_size=0.2, random_state=42):
    """
    Stage 4: Perform train/test split BEFORE fitting any preprocessing.
    Guarantees no data leakage between test and training partitions.
    """
    stratify_target = y if y.value_counts().min() >= 2 else None
    return train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=stratify_target,
    )


def fit_preprocessors(X_train):
    """
    Stages 5 & 6: Fit numerical and categorical preprocessing strictly on training data.
    - Numerical: SimpleImputer(median) -> StandardScaler()
    - Categorical: SimpleImputer(most_frequent) -> OneHotEncoder(handle_unknown='ignore')
    """
    # 5. Fit numerical preprocessing
    num_imputer = SimpleImputer(strategy="median")
    scaler = StandardScaler()
    imputed_num_train = num_imputer.fit_transform(X_train[NUMERICAL_FEATURES])
    scaler.fit(imputed_num_train)

    # 6. Fit categorical preprocessing
    cat_imputer = SimpleImputer(strategy="most_frequent")
    encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    imputed_cat_train = cat_imputer.fit_transform(X_train[CATEGORICAL_FEATURES])
    encoder.fit(imputed_cat_train)

    return {
        "num_imputer": num_imputer,
        "scaler": scaler,
        "cat_imputer": cat_imputer,
        "encoder": encoder,
    }


def transform_features(preprocessors, X):
    """
    Stage 7: Transform train/test data using pre-fitted transformers.
    Combines scaled numerical features and one-hot encoded categorical features.
    """
    num_imputer = preprocessors["num_imputer"]
    scaler = preprocessors["scaler"]
    cat_imputer = preprocessors["cat_imputer"]
    encoder = preprocessors["encoder"]

    # Transform numerical
    imputed_num = num_imputer.transform(X[NUMERICAL_FEATURES])
    scaled_num = scaler.transform(imputed_num)

    # Transform categorical
    imputed_cat = cat_imputer.transform(X[CATEGORICAL_FEATURES])
    encoded_cat = encoder.transform(imputed_cat)

    return np.hstack([scaled_num, encoded_cat])


def get_feature_names(preprocessors):
    """
    Retrieve feature names in exact order of the transformed matrix columns.
    """
    encoder = preprocessors["encoder"]
    cat_names = list(encoder.get_feature_names_out(CATEGORICAL_FEATURES))
    return NUMERICAL_FEATURES + cat_names


def train_model(X_train_processed, y_train, random_state=42):
    """
    Stage 8: Train Logistic Regression classifier.
    """
    model = LogisticRegression(max_iter=1000, random_state=random_state)
    model.fit(X_train_processed, y_train)
    return model


def evaluate_model(model, X_train_processed, y_train, X_test_processed, y_test):
    """
    Stages 9 & 10: Generate predictions and calculate evaluation metrics
    (accuracy, precision, recall, and training accuracy).
    """
    y_test_pred = model.predict(X_test_processed)
    y_train_pred = model.predict(X_train_processed)

    test_acc = accuracy_score(y_test, y_test_pred)
    test_prec = precision_score(y_test, y_test_pred, zero_division=0)
    test_rec = recall_score(y_test, y_test_pred, zero_division=0)

    train_acc = accuracy_score(y_train, y_train_pred)
    generalization_gap = train_acc - test_acc

    report = classification_report(y_test, y_test_pred, zero_division=0)

    return {
        "test_accuracy": round(float(test_acc), 4),
        "test_precision": round(float(test_prec), 4),
        "test_recall": round(float(test_rec), 4),
        "train_accuracy": round(float(train_acc), 4),
        "generalization_gap": round(float(generalization_gap), 4),
        "classification_report": report,
        "y_test_pred": y_test_pred,
        "y_train_pred": y_train_pred,
    }


def run_pipeline(data_path="data/churn_data.csv", random_state=42):
    """
    End-to-end execution across all 10 stages.
    """
    df = load_dataset(data_path)
    df_clean = clean_dataset(df)
    X, y = split_features_target(df_clean)

    X_train, X_test, y_train, y_test = split_data(
        X, y, test_size=0.2, random_state=random_state
    )

    preprocessors = fit_preprocessors(X_train)
    X_train_proc = transform_features(preprocessors, X_train)
    X_test_proc = transform_features(preprocessors, X_test)

    model = train_model(X_train_proc, y_train, random_state=random_state)
    evaluation = evaluate_model(model, X_train_proc, y_train, X_test_proc, y_test)
    feature_names = get_feature_names(preprocessors)

    coefficients = list(zip(feature_names, model.coef_[0]))
    coefficients_sorted = sorted(
        coefficients, key=lambda item: abs(item[1]), reverse=True
    )

    return {
        "dataset_size": len(df_clean),
        "class_distribution": df_clean[TARGET_COLUMN].value_counts().to_dict(),
        "train_size": len(X_train),
        "test_size": len(X_test),
        "preprocessors": preprocessors,
        "model": model,
        "evaluation": evaluation,
        "feature_names": feature_names,
        "coefficients": coefficients_sorted,
    }


if __name__ == "__main__":
    file_path = (
        sys.argv[1]
        if len(sys.argv) > 1
        else Path(__file__).resolve().parent.parent / "data" / "churn_data.csv"
    )
    results = run_pipeline(file_path)

    print("=" * 60)
    print("      LOGISTIC REGRESSION CHURN CLASSIFICATION")
    print("=" * 60)
    print(f"Dataset Size        : {results['dataset_size']} rows")
    print(f"Class Distribution  : {results['class_distribution']} (0: Retained, 1: Churned)")
    print(f"Train / Test Split  : {results['train_size']} train / {results['test_size']} test (80/20)")
    print("\n--- Test Set Metrics ---")
    print(f"Accuracy            : {results['evaluation']['test_accuracy']:.4f} ({results['evaluation']['test_accuracy'] * 100:.1f}%)")
    print(f"Precision           : {results['evaluation']['test_precision']:.4f} ({results['evaluation']['test_precision'] * 100:.1f}%)")
    print(f"Recall              : {results['evaluation']['test_recall']:.4f} ({results['evaluation']['test_recall'] * 100:.1f}%)")
    print("\n--- Overfitting Check ---")
    print(f"Training Accuracy   : {results['evaluation']['train_accuracy']:.4f}")
    print(f"Test Accuracy       : {results['evaluation']['test_accuracy']:.4f}")
    print(f"Generalization Gap  : {results['evaluation']['generalization_gap']:.4f}")
    print("\n--- Classification Report ---")
    print(results["evaluation"]["classification_report"])
    print("--- Logistic Regression Feature Coefficients ---")
    for name, coef in results["coefficients"]:
        sign = "+" if coef > 0 else "-"
        print(f"  {name:25s}: {sign}{abs(coef):.4f}")
    print("=" * 60)
