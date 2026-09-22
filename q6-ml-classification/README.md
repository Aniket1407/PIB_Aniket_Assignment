# Question 6: Machine Learning Churn Classification

A practical binary classification pipeline built with **scikit-learn** and **pandas** using **Logistic Regression** to predict customer churn (`will_churn`).

---

## 1. Problem Statement
The goal is to predict whether a customer will churn (`will_churn = 1`) or remain active (`will_churn = 0`) based on customer demographic details and behavioral engagement patterns.

---

## 2. Dataset & Features
The dataset contains 100 customer records with the following schema:

### Numerical Features:
- `Age`: Customer age in years.
- `income`: Annual income in USD.
- `number_of_logins`: Frequency of logins during the billing cycle.
- `purchase_count`: Number of completed purchases.
- `last_login_days`: Days elapsed since the customer last logged in.

### Categorical Feature:
- `subscription`: Tier category (`Free`, `Basic`, `Premium`).

### Target Variable:
- `will_churn`: Binary label (`0` = Retained, `1` = Churned).

---

## 3. Implementation Approach: 10 Explicit Stages
Rather than wrapping everything into a single opaque pipeline, the implementation in `src/train.py` is decomposed into 10 clean, transparent stages:

1. **Load the CSV**: Reads raw data using `pandas.read_csv`.
2. **Validate/Clean Dataset**: Validates required columns, drops exact duplicate rows, and standardizes target labels (handles `0`/`1` and `Yes`/`No`).
3. **Split X and y**: Separates feature matrix `X` from target vector `y`.
4. **Train / Test Split**: Splits into 80% train and 20% test partitions with `stratify=y` and `random_state=42`. **This split happens strictly before fitting preprocessors to eliminate data leakage.**
5. **Fit Numerical Preprocessing**: Fits `SimpleImputer(strategy='median')` and `StandardScaler()` strictly on `X_train[NUMERICAL_FEATURES]`.
6. **Fit Categorical Preprocessing**: Fits `SimpleImputer(strategy='most_frequent')` and `OneHotEncoder(handle_unknown='ignore', sparse_output=False)` strictly on `X_train[CATEGORICAL_FEATURES]`.
7. **Transform Train/Test Data**: Applies pre-fitted transformers to both `X_train` and `X_test`, then concatenates scaled numeric and encoded categorical features into dense arrays.
8. **Train Logistic Regression**: Fits `LogisticRegression(max_iter=1000, random_state=42)` on the transformed training data.
9. **Generate Predictions**: Computes binary class predictions for both test and training partitions.
10. **Calculate Evaluation Metrics**: Computes test Accuracy, Precision, Recall, and training accuracy for overfitting analysis.

---

## 4. Why Logistic Regression Was Selected
1. **Strong & Interpretable Baseline**: Logistic Regression is the standard industry baseline for binary classification. It outputs calibrated class probabilities via the sigmoid function ($\sigma(z) = \frac{1}{1 + e^{-z}}$) and direct feature log-odds coefficients.
2. **Explainable Coefficients**: Unlike black-box models, every feature has an interpretable weight: positive coefficients increase churn probability, while negative coefficients decrease churn probability.
3. **Low Computational Overhead & Zero Risk of Complex Overfitting**: For tabular datasets of moderate size, deep models or deep decision trees easily memorize noise. Logistic Regression with default L2 regularization converges in milliseconds and generalizes reliably.
4. **Reproducible**: Convex optimization guarantees convergence to a global optimum without seed sensitivity issues.

---

## 5. Why Feature Scaling is Essential for Logistic Regression
- Decision trees split features independently, but Logistic Regression computes a weighted linear sum:
  $$z = w_1 x_1 + w_2 x_2 + \dots + b$$
- If `income` ranges from \$20,000 to \$110,000 while `purchase_count` ranges from 0 to 10, the gradient descent step and L2 penalty would disproportionately penalize or depend on the high-magnitude feature.
- `StandardScaler` standardizes each feature to zero mean and unit variance ($\mu = 0, \sigma = 1$), ensuring fair regularization and fast gradient convergence.

---

## 6. Actual Observed Evaluation Results

Evaluated on the held-out 20-sample test set (`random_state=42`, `stratify=y`):

| Metric | Score | Description |
|---|---|---|
| **Test Accuracy** | **1.0000** (100.0%) | Proportion of correct classifications overall. |
| **Test Precision** | **1.0000** (100.0%) | TP / (TP + FP) for churners. |
| **Test Recall** | **1.0000** (100.0%) | TP / (TP + FN) for churners. |
| **Training Accuracy** | **1.0000** (100.0%) | Performance on the training split. |
| **Generalization Gap** | **0.0000** (0.0%) | `train_accuracy - test_accuracy`. |

### Test Classification Report:
```text
              precision    recall  f1-score   support

           0       1.00      1.00      1.00        14
           1       1.00      1.00      1.00         6

    accuracy                           1.00        20
   macro avg       1.00      1.00      1.00        20
weighted avg       1.00      1.00      1.00        20
```

### Feature Coefficients (Log-Odds Impact on Churn):
| Feature | Coefficient | Interpretation |
|---|---|---|
| `last_login_days` | **+2.0733** | Strongest churn indicator: more inactive days substantially increases churn risk. |
| `number_of_logins` | **-1.3122** | Strong retention indicator: frequent logins protect against churn. |
| `purchase_count` | **-0.9988** | Strong retention indicator: active buyers are far less likely to churn. |
| `Age` | **+0.4180** | Older customers show slightly higher churn tendency in this dataset. |
| `subscription_Basic` | **+0.1946** | Basic tier subscribers have slightly higher churn tendency than average. |
| `subscription_Free` | **-0.1659** | Free tier subscribers. |
| `income` | **+0.1578** | Minor positive correlation. |
| `subscription_Premium` | **-0.0298** | Premium tier subscribers have slightly lower churn tendency. |

---

## 7. Class Distribution & Imbalance Discussion
- **Class 0 (Retained)**: 68 samples (68.0%)
- **Class 1 (Churned)**: 32 samples (32.0%)
- **Why Accuracy Alone Is Insufficient**: In churn problems, retained users usually outnumber churned users. A naive model predicting "Retained" for every single customer would achieve 68% accuracy while missing 100% of churners.
- **Why Recall is Crucial for Churn**: False Negatives (predicting an at-risk customer will stay when they actually leave) are costly for businesses because no retention intervention is triggered. High Recall ensures at-risk customers are successfully identified.

---

## 8. Overfitting Assessment
- **Training Accuracy**: 1.0000
- **Test Accuracy**: 1.0000
- **Generalization Gap**: 0.0000
- **Assessment**: Because the dataset is a clean, representative sample where inactivity (`last_login_days`) and low engagement (`number_of_logins`) cleanly separate churners, Logistic Regression found an optimal linear separating hyperplane. There is no evidence of runaway overfitting (training accuracy is not higher than test accuracy). However, because the test set contains 20 samples, each individual prediction accounts for 5% of accuracy. On larger and noisier production data, slight metric degradation is expected.

---

## 9. Possible Improvements for Production
1. **More Training Data**: Expanding the dataset from 100 to 10,000+ records will improve variance stability and expose edge cases.
2. **K-Fold Stratified Cross-Validation**: Use 5-fold or 10-fold cross-validation (`StratifiedKFold`) to measure metric variance across multiple partitions.
3. **Hyperparameter Regularization Tuning**: Tune the inverse regularization strength $C$ using `GridSearchCV(LogisticRegression(), param_grid={'C': [0.01, 0.1, 1.0, 10.0]})`.
4. **Feature Engineering**:
   - Engagement intensity: `logins_per_active_day = number_of_logins / (last_login_days + 1)`
   - Spending rate: `income_to_purchase_ratio = income / (purchase_count + 1)`
5. **Classification Threshold Tuning**: In high-churn-risk businesses, lowering the classification threshold from 0.5 to 0.3 increases Recall, capturing more churners at the cost of slight precision drops.
6. **Class-Weight Adjustment**: If class imbalance becomes severe (e.g. 95% retained vs 5% churned), configure `class_weight='balanced'`.
7. **Tree-Based Ensembles**: Benchmark against LightGBM or Random Forest to test for non-linear interactions.
8. **Model Monitoring**: Track distribution drift (e.g. using Kolmogorov-Smirnov test on input features) once deployed.

---

## 10. Setup & Execution

### Prerequisites:
- Python 3.10+
- Packages in `requirements.txt` (`pandas`, `scikit-learn`, `pytest`).

### Run Training Pipeline:
```bash
cd q6-ml-classification
python3 src/train.py
```

### Run Automated Tests:
```bash
pytest tests/test_model.py -v
```
All 11 unit tests verify:
1. Dataset contains expected columns.
2. Target is separated correctly.
3. Train/test split works.
4. Preprocessing can be fitted on training data.
5. Logistic Regression can be trained.
6. Predictions are generated.
7. Predictions contain valid binary values.
8. Accuracy can be calculated.
9. Precision can be calculated.
10. Recall can be calculated.
11. Missing feature values are handled by the preprocessing logic.
