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
**None.** Diagnosed and solved independently based on React best practices.\n