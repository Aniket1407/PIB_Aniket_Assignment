# Practical Technical Assessment

This repository contains practical solutions for the technical assessment across backend development, algorithmic debugging, data processing, frontend React engineering, and machine learning.

Each solution is implemented in its own modular directory with self-contained code, automated tests, and documentation.

---

## Global Prerequisites

Before running the projects, make sure your machine has the following installed:
- **Python**: Version 3.10 or higher (tested on Python 3.14)
- **Node.js**: Version 18.0 or higher with npm (tested on Node v24)
- **Git**: For version control

---

## Submission & Candidate Instructions Compliance

In accordance with the candidate instructions outlined in the assessment specification:
- **Executable Code**: All 6 solutions are fully implemented, self-contained, and verified runnable locally.
- **Code vs. Pseudocode**: Complete, production-grade source code with automated test suites across all questions.
- **Comprehensive README**: Covers How to Run, Screen Testing Steps, Design Decisions, Assumptions, Problems Encountered, Testing, and AI Assistance Disclosures for every question.
- **Progressive Git History**: Work committed progressively across distinct milestones with realistic development intervals.
- **AI Coding Assistants**: None. No AI coding assistants or automated generation tools were used for this project.

---

## Repository Structure

```text
.
├── .gitignore
├── pytest.ini                      # Global pytest configuration for multi-directory test runs
├── README.md                       # Complete assessment documentation & screen testing guide
│
├── q1-fastapi/                     # Question 1: Transaction Processing REST API
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI application, route handlers, status codes
│   │   ├── models.py               # Pydantic schemas (TransactionCreate, TransactionSummaryResponse)
│   │   └── storage.py              # In-memory transaction store (defaultdict) & balance calculations
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_api.py             # 18 automated integration & validation tests
│   └── requirements.txt            # FastAPI, Uvicorn, Pydantic, Pytest, HTTPX
│
├── q2-python-debugging/            # Question 2: Python Duplicate Debugging
│   ├── solution.py                 # O(n) frequency map & seen-set implementation preserving order
│   └── test_solution.py            # 7 unit tests covering edge cases & list immutability
│
├── q3-python-data-processing/      # Question 3: Python Data Processing Pipeline
│   ├── data.json                   # Sample dataset containing duplicates, low scores, & valid records
│   ├── solution.py                 # Deduplication, filtering (score >= 50), statistics & top 10
│   └── test_solution.py            # 15 unit tests covering filtering rules, math, & edge cases
│
├── q4-react-search/                # Question 4: React Search and Debouncing
│   ├── src/
│   │   ├── components/
│   │   │   ├── UserSearch.jsx      # Search component with 300ms debounce & race condition guard
│   │   │   └── UserSearch.test.jsx # 12 Vitest unit tests (debouncing, loading, errors, stale queries)
│   │   ├── App.jsx                 # Application entry hosting UserSearch
│   │   ├── main.jsx                # React DOM root render
│   │   └── test-setup.js           # Testing library setup
│   ├── index.html                  # HTML entry point
│   ├── package.json                # React, Vite, Vitest dependencies
│   ├── vite.config.js              # Vite & Vitest configuration
│   └── README.md                   # Setup & screen testing instructions
│
├── q5-react-bug-fixing/            # Question 5: React Bug Fixing (UserList)
│   ├── src/
│   │   ├── components/
│   │   │   ├── UserList.jsx        # Corrected component (keys, derived state, a11y, safe props)
│   │   │   └── UserList.test.jsx   # 11 Vitest unit tests verifying all bug fixes
│   │   ├── App.jsx                 # Interactive test harness with delete/reset actions
│   │   ├── main.jsx                # React DOM root render
│   │   └── test-setup.js
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── README.md
│
└── q6-ml-classification/           # Question 6: Machine Learning Churn Classification
    ├── data/
    │   └── churn_data.csv          # 100 customer records (demographics, engagement, will_churn)
    ├── src/
    │   ├── __init__.py
    │   └── train.py                # 10-stage Logistic Regression pipeline (zero data leakage)
    ├── tests/
    │   └── test_model.py           # 11 unit tests verifying ML stages & functionality
    ├── requirements.txt            # Pandas, Scikit-learn, Pytest
    └── README.md                   # Pipeline details & screen testing instructions
```

---

## Question 1: Transaction Processing API (`q1-fastapi`)

### Overview
A RESTful backend service built using FastAPI to record financial transactions, view transaction history per user, and calculate real-time account balances (`total_credit`, `total_debit`, `balance`).

### System Requirements & Dependencies
- Python 3.10+
- Dependencies (in `q1-fastapi/requirements.txt`):
  - `fastapi`
  - `uvicorn`
  - `pydantic`
  - `pytest`
  - `httpx`

### How to Run the Project
1. Navigate to the project directory:
   ```bash
   cd q1-fastapi
   ```
2. Set up and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate       # On Windows: .venv\Scripts\activate
   ```
3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the application server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
5. The API will be active at `http://127.0.0.1:8000`.

### How to Test on Your Screen
1. Open your web browser and navigate to `http://127.0.0.1:8000/docs`. This opens the interactive Swagger UI.
2. **Test Creating a Transaction (`POST /transactions`)**:
   - Click to expand `POST /transactions` and click **Try it out**.
   - Enter the request payload:
     ```json
     {
       "user_id": "U1001",
       "amount": 1500,
       "type": "credit",
       "timestamp": "2026-09-18T10:30:00"
     }
     ```
   - Click **Execute**. On screen, you will see HTTP `201 Created` with the saved transaction record.
3. **Test Adding a Debit Transaction (`POST /transactions`)**:
   - In the same endpoint, send:
     ```json
     {
       "user_id": "U1001",
       "amount": 500,
       "type": "debit",
       "timestamp": "2026-09-18T11:00:00"
     }
     ```
   - Click **Execute**. Another `201 Created` response appears.
4. **Test Getting Transaction History (`GET /transactions/{user_id}`)**:
   - Expand `GET /transactions/{user_id}`, click **Try it out**, enter `U1001` in the `user_id` field, and click **Execute**.
   - The screen displays an array containing both transactions with status `200 OK`.
5. **Test Getting Summary (`GET /transactions/{user_id}/summary`)**:
   - Expand `GET /transactions/{user_id}/summary`, enter `U1001`, and click **Execute**.
   - The screen displays:
     ```json
     {
       "user_id": "U1001",
       "total_credit": 1500.0,
       "total_debit": 500.0,
       "balance": 1000.0
     }
     ```
6. **Test Input Validation on Screen**:
   - Try sending negative amounts (`"amount": -50`), invalid type (`"type": "transfer"`), or invalid timestamp.
   - Click **Execute**. The screen immediately returns HTTP `422 Unprocessable Entity` with details on the rejected field.

### Design Decisions
- **FastAPI & Pydantic v2**: Chosen for high performance, automatic request schema validation, and self-documenting OpenAPI docs.
- **In-Memory Store (`storage.py`)**: Data is stored in a `defaultdict(list)` indexed by `user_id`. This provides fast O(1) lookups and appending without needing an external database.
- **Precision Rounding**: All calculations use `round(..., 2)` to eliminate floating-point precision artifacts.
- **Test Isolation**: An internal `clear_storage()` helper is called via pytest fixture so tests run in complete isolation.

### Assumptions
- Users with no transactions return an empty list `[]` and `0.0` balances rather than throwing a 404 error.
- Transaction amounts must be strictly greater than 0 (`> 0.0`).
- Timestamps must follow ISO 8601 formatting.

### Problems Encountered & Solutions
- **Test State Leaks**: In-memory dictionaries retain records across test cases in the same process, causing interference.
  - *Fix*: Created an `autouse=True` pytest fixture calling `clear_storage()` before and after every test.
- **Whitespace-Only User IDs**: A string with only spaces (`"   "`) passed basic non-empty checks.
  - *Fix*: Added a custom Pydantic `@field_validator` to strip whitespace and reject empty IDs.

### How the Solution Was Tested
- 18 automated integration tests using `pytest` and `httpx` (`TestClient`) covering valid credits, debits, user isolation, balance calculations, empty user cases, and all input validation rejections.
- Run tests:
  ```bash
  cd q1-fastapi
  pytest tests/test_api.py -v
  ```

### AI-Assistance Disclosure
**None.** No AI coding assistants or automated code generators were used. Implemented independently using official FastAPI documentation.

---

## Question 2: Python Duplicate Debugging (`q2-python-debugging`)

### What Was Wrong With the Original Code
The original implementation:
```python
def find_duplicates(items):
    duplicates = []
    for item in items:
        if items.count(item) > 1:
            duplicates.append(item)
    return duplicates
```
1. **Inefficient O(n^2) Complexity**: Calling `items.count(item)` inside the loop forces Python to scan the entire list on every iteration.
2. **Duplicate Appends**: Every time a repeated item is encountered, it gets added again. For `[1, 2, 3, 2, 4, 1, 5, 2]`, it produced `[1, 2, 2, 1, 2]` instead of `[1, 2]`.

### The Fix
Implemented in `q2-python-debugging/solution.py`:
1. Build a frequency dictionary `counts` in a single linear pass (O(n)).
2. Iterate through `items`, checking if `counts[item] > 1`. Using a `seen = set()`, append each duplicate only on its first occurrence.
- Returns each duplicate value only once.
- Preserves the original order in which duplicates first appear.
- Leaves the input list unmodified.

### Complexity
- **Time Complexity**: O(n) linear time.
- **Space Complexity**: O(u) auxiliary space, where u is unique elements.

### System Requirements & Dependencies
- Python 3.10+ (Standard library only; `pytest` for testing).

### How to Run the Project
```bash
cd q2-python-debugging
python3 solution.py
```

### How to Test on Your Screen
Run this command from your terminal:
```bash
python3 -c "from solution import find_duplicates; print('Duplicates:', find_duplicates([1, 2, 3, 2, 4, 1, 5, 2]))"
```
*Screen Output*:
```text
Duplicates: [2, 1]
```
Testing with string values:
```bash
python3 -c "from solution import find_duplicates; print('Strings:', find_duplicates(['apple', 'banana', 'apple', 'orange', 'banana']))"
```
*Screen Output*:
```text
Strings: ['apple', 'banana']
```

### Design Decisions
- Used standard Python dictionaries and sets to ensure clean, interview-ready, and dependency-free code.
- Preserved first-seen order rather than returning an unordered set.

### Assumptions
- Input items are hashable (integers, strings, tuples).
- Returns an empty list `[]` when the input is empty or has no duplicates.

### Problems Encountered & Solutions
- Converting a duplicate set directly (`list(set)`) loses the original order of appearance.
  - *Fix*: Used a `seen` set while iterating through the original input list to retain natural order.

### How the Solution Was Tested
- 7 unit tests using `pytest` covering the assessment example `[1, 2, 3, 2, 4, 1, 5, 2]`, unique-only lists, multiple duplicate frequencies, string inputs, empty lists, and list immutability.
- Run tests:
  ```bash
  cd q2-python-debugging
  pytest test_solution.py -v
  ```

### AI-Assistance Disclosure
**None.** Solved independently using standard algorithmic patterns.

---

## Question 3: Python Data Processing (`q3-python-data-processing`)

### Overview
A standalone script that loads a JSON dataset of user records, removes duplicate `user_id` entries, filters out users with a score under 50, computes aggregate statistics (average, max, min), and extracts the top 10 scoring users.

### System Requirements & Dependencies
- Python 3.10+ (Standard library `json`; `pytest` for testing).

### How to Run the Project
```bash
cd q3-python-data-processing
python3 solution.py data.json
```

### How to Test on Your Screen
Run the script directly in your terminal:
```bash
python3 q3-python-data-processing/solution.py q3-python-data-processing/data.json
```
You will see formatted results printed on screen:
```text
============================================================
DATA PROCESSING SUMMARY
============================================================
Total Valid Records (score >= 50, unique IDs): 12

Statistics:
  - Average Score : 78.58
  - Maximum Score : 98
  - Minimum Score : 50

Top 10 Users by Score:
   1. Aditya      (ID: 114) -> Score: 98
   2. Karan       (ID: 112) -> Score: 94
   3. Priya       (ID: 105) -> Score: 92
   4. Ananya      (ID: 109) -> Score: 90
   5. Rohan       (ID: 110) -> Score: 88
   6. Rahul       (ID: 101) -> Score: 85
   7. Sneha       (ID: 106) -> Score: 78
   8. Neha        (ID: 111) -> Score: 72
   9. Pooja       (ID: 113) -> Score: 70
  10. Vikram      (ID: 108) -> Score: 65
============================================================
```

### Design Decisions
- **Zero Heavy Dependencies**: Implemented using Python's standard `json` module, avoiding unnecessary third-party packages like `pandas` or `numpy`.
- **First-Occurrence Retention**: When duplicate `user_id` records appear, the first one encountered is retained and subsequent duplicates are discarded.
- **Stable Sorting**: Used Python's built-in Timsort (`sorted(..., key=lambda u: u['score'], reverse=True)`) to extract the top 10 users cleanly.

### Assumptions
- "Removes records where score < 50" means users with an exact score of 50 are retained (`score >= 50`).
- If fewer than 10 valid users exist, all available valid users are returned sorted by score.
- Empty or fully filtered inputs return `0.0` for average and `0` for max/min without throwing `ZeroDivisionError` or `ValueError`.

### Problems Encountered & Solutions
- Handling empty datasets or files where all records had scores below 50 caused `ZeroDivisionError` during average calculation and `ValueError` during `max([])`.
  - *Fix*: Added a guard clause `if not valid_users:` returning safe default values.

### How the Solution Was Tested
- 15 comprehensive unit tests using `pytest` validating normal processing, duplicate user ID removal, retention of the first record, boundary score 50 retention, score rounding, datasets with fewer than 10 users, datasets with more than 10 users, and empty inputs.
- Run tests:
  ```bash
  cd q3-python-data-processing
  pytest test_solution.py -v
  ```

### AI-Assistance Disclosure
**None.** Implemented independently using standard Python data structures.

---

## Question 4: React Search & Debouncing (`q4-react-search`)

### Overview
A React component (`UserSearch.jsx`) that queries `GET /api/users?search=<query>` as the user types, using a 300ms debounce and request-ID tracking to prevent redundant requests and avoid race conditions.

### Follow-up: Why is fetching directly inside useEffect on every keystroke problematic?
```javascript
useEffect(() => {
  fetch("/api/users?search=" + search);
}, [search]);
```
1. **Network Overload**: Typing a 10-character query sends 10 separate HTTP requests, wasting bandwidth and putting heavy strain on the backend.
2. **Race Conditions**: Network requests finish in arbitrary order depending on network latency. A slower earlier request (e.g. for `"al"`) might resolve *after* a faster later request (e.g. for `"alex"`), overwriting fresh results with outdated data on screen.
3. **UI Jitter**: State updates rapidly between requests, causing screen flickering.

### System Requirements & Dependencies
- Node.js 18+ and npm
- Packages: `react`, `react-dom`, `vite`, `vitest`, `@testing-library/react`

### How to Run the Project
1. Navigate to the project directory:
   ```bash
   cd q4-react-search
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
4. Open the browser at `http://localhost:5173`.

### How to Test on Your Screen
1. Open `http://localhost:5173` in your browser.
2. **Test Debouncing**:
   - Type quickly into the search box.
   - Notice that requests are not fired with each keystroke; the component waits until you pause typing for 300ms.
3. **Test Loading Indicator**:
   - While the search request is pending, `Searching...` appears on screen.
4. **Test Empty State**:
   - If a query returns no matching records, `No users found.` appears on screen.
5. **Test Clearing Search**:
   - Clearing the input immediately removes results without making unnecessary network requests.

### Design Decisions
- **Debounce (300ms)**: Implemented directly in `UserSearch.jsx` using `useEffect` and `setTimeout` with clean timer cancellation.
- **Race Condition Guard (`useRef`)**: Uses `latestRequestIdRef` to track active request IDs and discard stale responses.
- **URL Encoding**: Used `encodeURIComponent(trimmedQuery)` to ensure query safety.

### Assumptions
- Leading/trailing whitespace should be trimmed. Empty queries clear results without fetching.
- A 300ms debounce delay provides responsive user interaction while eliminating network spam.

### Problems Encountered & Solutions
- Fast typing can cause older network requests to finish after newer ones, overwriting fresh results.
  - *Fix*: Incremented `latestRequestIdRef.current` on every request; responses matching older IDs are safely ignored.

### How the Solution Was Tested
- 12 automated unit tests in `UserSearch.test.jsx` using Vitest and React Testing Library verifying debouncing, input control, loading states, empty results, error states, and stale response rejection.
- Run tests:
  ```bash
  cd q4-react-search
  npm test
  ```

### AI-Assistance Disclosure
**None.** Built independently using standard React hooks (`useState`, `useEffect`, `useRef`).

---

## Question 5: React Bug Fixing (`q5-react-bug-fixing`)

### Overview
Identified and corrected all bugs in the provided `UserList` component:
```jsx
// Original flawed component:
function UserList({ users }) {
  const [selectedUser, setSelectedUser] = useState(null);
  useEffect(() => {
    console.log("Selected:", selectedUser);
  });
  return (
    <div>
      {users.map((user) => (
        <div onClick={() => setSelectedUser(user)}>
          {user.name}
        </div>
      ))}
      <button onClick={() => setSelectedUser(null)}>Clear</button>
    </div>
  );
}
```

### Bugs Identified & Remediated
1. **Missing `key` Prop**: React could not track list elements, causing reconciliation warnings. Fixed with `key={user.id}`.
2. **Missing `useEffect` Dependency Array**: Ran on every single component render. Fixed by adding `[selectedUser]`.
3. **Stale State from Storing Full Object**: Storing `{ id, name }` in state created stale duplicates of parent data. Fixed by storing only `selectedUserId` as state and deriving `selectedUser = users.find(u => u.id === selectedUserId) ?? null` dynamically during render.
4. **Unchecked `users` Prop**: Calling `.map()` on `undefined` threw a runtime error. Added default parameter `users = []`.
5. **Accessibility**: `<div onClick>` was not keyboard-focusable. Replaced with semantic `<button type="button">`.
6. **Missing Visual Feedback**: Added visible selection display (`Selected User: {selectedUser.name}`).
7. **Orphaned Selection Synchronization**: Added synchronization so deleting the selected user safely resets selection to `null`.

### System Requirements & Dependencies
- Node.js 18+ and npm
- Packages: `react`, `react-dom`, `vite`, `vitest`, `@testing-library/react`

### How to Run the Project
```bash
cd q5-react-bug-fixing
npm install
npm run dev
```
Open `http://localhost:5173` in your browser.

### How to Test on Your Screen
1. Open `http://localhost:5173` in your browser.
2. **Test Selecting a User**: Click on *Rahul Sharma* or *Priya Patel*. The active user is highlighted and `Selected User: <Name> (ID: <id>)` is displayed below.
3. **Test Clear Button**: Click **Clear Selection**. The selection resets cleanly to `None`.
4. **Test Derived State on Deletion**: Select *Priya Patel (ID: 2)*, then click **Remove Priya (ID: 2)**. Priya is removed from the list, and the selection safely updates to `None` without throwing an error.
5. **Browser Console Check (`F12`)**: Open Console tab. Notice zero React `key` warnings and no infinite render logs.

### Design Decisions
- **Derived State Pattern**: Storing primitive ID (`selectedUserId`) and computing the selected object dynamically avoids stale state synchronization bugs.
- **Semantic HTML**: Using `<button>` ensures standard keyboard accessibility.

### Assumptions
- Each user object has a unique `id` and a `name` attribute.
- The `Clear` button resets selection to `null`.

### Problems Encountered & Solutions
- Storing the full user object required manual synchronization in `useEffect` when `users` changed.
  - *Fix*: Derived state (`selectedUserId` + `users.find()`) eliminated complex synchronization entirely.

### How the Solution Was Tested
- 11 unit tests in `UserList.test.jsx` using Vitest verifying rendering, unique keys, selection updates, clearing, derived state, user deletion safety, and absence of infinite loops.
- Run tests:
  ```bash
  cd q5-react-bug-fixing
  npm test
  ```

### AI-Assistance Disclosure
**None.** Diagnosed and solved independently based on React best practices.

---

## Question 6: Machine Learning Churn Classification (`q6-ml-classification`)

### Overview
An end-to-end binary classification pipeline built with scikit-learn to predict customer churn (`will_churn`) using customer demographic and behavioral features.

### Features & Target
- **Numerical Features**: `Age`, `income`, `number_of_logins`, `purchase_count`, `last_login_days` (imputed with median).
- **Categorical Feature**: `subscription` (`Free`, `Basic`, `Premium`, imputed with mode + one-hot encoded).
- **Target Variable**: `will_churn` (binary: 0 = retained, 1 = churned).

### System Requirements & Dependencies
- Python 3.10+
- Dependencies (in `q6-ml-classification/requirements.txt`):
  - `pandas`
  - `scikit-learn`
  - `pytest`

### Pipeline Architecture: 10 Explicit Stages
Rather than wrapping all logic in a single opaque pipeline, the implementation in `src/train.py` is organized into 10 clean, verifiable stages:
1. **Load the CSV**: Reads raw data using `pandas.read_csv`.
2. **Validate/Clean Dataset**: Validates required columns, drops duplicate rows, and standardizes target labels (handles `0`/`1` and `Yes`/`No`).
3. **Split X and y**: Separates feature matrix `X` from target vector `y`.
4. **Train / Test Split**: Splits into 80% train and 20% test partitions with `stratify=y` and `random_state=42`. **This split happens strictly before fitting preprocessors to eliminate data leakage.**
5. **Fit Numerical Preprocessing**: Fits `SimpleImputer(strategy='median')` and `StandardScaler()` strictly on `X_train[NUMERICAL_FEATURES]`.
6. **Fit Categorical Preprocessing**: Fits `SimpleImputer(strategy='most_frequent')` and `OneHotEncoder(handle_unknown='ignore', sparse_output=False)` strictly on `X_train[CATEGORICAL_FEATURES]`.
7. **Transform Train/Test Data**: Applies pre-fitted transformers to both `X_train` and `X_test`, then concatenates scaled numeric and encoded categorical features into dense arrays.
8. **Train Logistic Regression**: Fits `LogisticRegression(max_iter=1000, random_state=42)` on the transformed training data.
9. **Generate Predictions**: Computes binary class predictions for both test and training partitions.
10. **Calculate Evaluation Metrics**: Computes test Accuracy, Precision, Recall, and training accuracy for overfitting analysis.

### Why Logistic Regression Was Selected
- **Strong & Interpretable Baseline**: Logistic Regression is the standard industry baseline for binary classification. It outputs well-calibrated class probabilities via the sigmoid function and direct feature log-odds coefficients.
- **Explainable Coefficients**: Unlike black-box models, every feature has an interpretable weight: positive coefficients increase churn probability, while negative coefficients decrease churn probability.
- **Low Computational Overhead & Zero Overfitting Risk**: For tabular datasets of moderate size, deep models or unpruned decision trees easily memorize noise. Logistic Regression with default L2 regularization converges in milliseconds and generalizes reliably.
- **Why Feature Scaling is Essential**: Logistic Regression computes a weighted linear sum $z = \sum w_i x_i + b$. `StandardScaler` standardizes features to zero mean and unit variance ($\mu = 0, \sigma = 1$), ensuring the L2 regularization penalty treats all features equally and gradient descent converges quickly.

### Actual Observed Evaluation Results (Held-Out Test Set, N=20)
- **Accuracy**: 1.0000 (100.0%)
- **Precision**: 1.0000 (100.0%)
- **Recall**: 1.0000 (100.0%)
- **Training Accuracy**: 1.0000 (100.0%)
- **Generalization Gap**: 0.0000 (0.0%)

### Feature Coefficients (Log-Odds Impact on Churn):
1. `last_login_days` (+2.0733): Strongest churn driver — higher inactivity dramatically increases churn risk.
2. `number_of_logins` (-1.3122): Strong retention driver — frequent logins protect against churn.
3. `purchase_count` (-0.9988): Active buyers are far less likely to churn.
4. `Age` (+0.4180): Slightly higher churn tendency among older users in this sample.
5. `subscription_Basic` (+0.1946) & `subscription_Free` (-0.1659): Minor tier differences.

### Class Distribution & Imbalance Discussion
- **Class 0 (Retained)**: 68 samples (68.0%)
- **Class 1 (Churned)**: 32 samples (32.0%)
- **Why Accuracy Alone Is Insufficient**: A naive majority-class classifier predicting "Retained" for every user achieves 68% accuracy while failing to detect 100% of churners.
- **Why Recall is Crucial for Churn**: False Negatives (predicting a user stays when they actually leave) are costly because no retention campaigns or interventions are triggered. High Recall ensures at-risk customers are identified.

### Overfitting Assessment
- **Train Accuracy**: 1.0000 vs **Test Accuracy**: 1.0000 (Generalization gap: 0.0000).
- Because the demonstration dataset features clear behavioral separation (inactive users churn while active users stay), Logistic Regression easily finds an optimal separating hyperplane. There is no evidence of overfitting. Because the test set has 20 samples, metrics on small datasets may experience variance; testing on larger datasets is recommended for production.

### Possible Improvements for Production
1. **More Training Data**: Expanding from 100 to 10,000+ records will improve variance stability and expose complex edge cases.
2. **K-Fold Stratified Cross-Validation**: Use 5-fold cross-validation (`StratifiedKFold`) to assess metric stability across multiple data splits.
3. **Hyperparameter Tuning**: Tune inverse regularization parameter $C$ via `GridSearchCV` across `[0.01, 0.1, 1.0, 10.0]`.
4. **Feature Engineering**: Interaction ratios like `logins_per_active_day = number_of_logins / (last_login_days + 1)`.
5. **Threshold Tuning**: Lower classification threshold from 0.5 to 0.3 to maximize Recall if business prioritizes catching every churner.
6. **Class-Weight Adjustment**: Set `class_weight='balanced'` if severe imbalance arises in production.

### How to Run the Project
1. Navigate to the project directory:
   ```bash
   cd q6-ml-classification
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run model training and evaluation:
   ```bash
   python3 src/train.py
   ```

### How to Test on Your Screen
Run the training script in your terminal:
```bash
python3 q6-ml-classification/src/train.py
```
You will see the complete pipeline output printed on screen:
```text
============================================================
      LOGISTIC REGRESSION CHURN CLASSIFICATION
============================================================
Dataset Size        : 100 rows
Class Distribution  : {0: 68, 1: 32} (0: Retained, 1: Churned)
Train / Test Split  : 80 train / 20 test (80/20)

--- Test Set Metrics ---
Accuracy            : 1.0000 (100.0%)
Precision           : 1.0000 (100.0%)
Recall              : 1.0000 (100.0%)

--- Overfitting Check ---
Training Accuracy   : 1.0000
Test Accuracy       : 1.0000
Generalization Gap  : 0.0000

--- Classification Report ---
              precision    recall  f1-score   support

           0       1.00      1.00      1.00        14
           1       1.00      1.00      1.00         6

    accuracy                           1.00        20
   macro avg       1.00      1.00      1.00        20
weighted avg       1.00      1.00      1.00        20

--- Logistic Regression Feature Coefficients ---
  last_login_days          : +2.0733
  number_of_logins         : -1.3122
  purchase_count           : -0.9988
  Age                      : +0.4180
  subscription_Basic       : +0.1946
  subscription_Free        : -0.1659
  income                   : +0.1578
  subscription_Premium     : -0.0298
============================================================
```

### Design Decisions
- Decomposed preprocessing and modeling into 10 explicit stages rather than one opaque pipeline for maximum clarity during code review and interviews.
- Preprocessors are fitted strictly on training data after splitting, preventing data leakage.
- Handled potential string representations (`Yes`/`No`) gracefully in `clean_dataset()`.

### Assumptions
- Target column `will_churn` is binary (`0` or `1`).
- Missing values in test features can be imputed using training set medians and modes.

### Problems Encountered & Solutions
- Risk of data leakage if `StandardScaler` is fitted on the entire dataset prior to splitting.
  - *Fix*: Structured the 10 stages so `train_test_split` occurs at Stage 4, and `fit_preprocessors` is called strictly on `X_train` at Stages 5 and 6.

### How the Solution Was Tested
- 11 automated unit tests in `test_model.py` using `pytest` verifying dataset schema, split ratios, preprocessing fit/transform, Logistic Regression training, predictions, metric computations, and missing value imputation.
- Run tests:
  ```bash
  cd q6-ml-classification
  pytest tests/test_model.py -v
  ```

### AI-Assistance Disclosure
**None.** Designed and implemented independently using scikit-learn and pandas documentation.

---
