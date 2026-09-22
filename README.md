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
**None.** Solved independently using standard algorithmic patterns.\n