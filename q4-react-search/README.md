# Question 4: React Search and Debouncing

A robust and interview-friendly React search component implemented under `q4-react-search/src/components/UserSearch.jsx`.

---

## 1. Component Behavior

- **Controlled Search Input**: Text input state is managed via `search` in React `useState`.
- **Debounced Updates**: Typing does not trigger network requests immediately. Changes propagate to a `debouncedSearch` state only after the user stops typing for 300ms.
- **Empty Query Handling**: When the input is cleared or consists only of whitespace, the search is cancelled, previous results and errors are cleared, and loading is set to `false` without making any network request.
- **UI States**:
  1. *Initial State*: Clean input ready for typing.
  2. *Loading State*: Displays `Searching...` while a request is in flight.
  3. *Results State*: Renders user cards showing name and email, keyed by unique `user.id`.
  4. *No Results State*: Displays `No users found.` only when a search has resolved with an empty array.
  5. *Error State*: Displays user-friendly fallback `Something went wrong. Please try again.` on HTTP error status (non-2xx) or network failures.

---

## 2. Debounce Implementation

- **Delay Constant**: `const DEBOUNCE_DELAY = 300;` (300 milliseconds).
- Implemented directly in `UserSearch.jsx` using `useEffect` and `setTimeout` (no external hooks or libraries):
  ```javascript
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedSearch(search);
    }, DEBOUNCE_DELAY);

    return () => {
      clearTimeout(timer);
    };
  }, [search]);
  ```
- **Cleanup**: Every keystroke clears the previous pending timer via `clearTimeout(timer)` before starting a new one. Unmounting the component also runs the cleanup callback, preventing memory leaks or state updates on unmounted components.

---

## 3. Stale Response & Race Condition Handling (Request ID Counter)

Network requests can resolve out-of-order due to network latency fluctuations:
- Request 1 (`search="jo"`) might take 800ms.
- Request 2 (`search="john"`) might take 200ms.

Without protection, Request 1 resolving after Request 2 would overwrite newer search results with outdated data.

### Request ID Mechanism (`useRef`):
1. A mutable sequence counter `latestRequestIdRef = useRef(0)` tracks the most recent request sequence number.
2. When a search effect starts:
   ```javascript
   const currentRequestId = ++latestRequestIdRef.current;
   ```
3. When the async fetch resolves or errors:
   ```javascript
   if (currentRequestId !== latestRequestIdRef.current) {
     return; // Discard stale response
   }
   ```
4. If a newer request has begun (`latestRequestIdRef.current > currentRequestId`), the older completion is completely ignored and will neither update `users`, toggle `loading`, nor surface an error.

---

## 4. Why is Directly Calling Fetch in `useEffect` on Every Keystroke Problematic?

1. **Massive Unnecessary Network Traffic**: Typing a word like `"developer"` fires 9 individual HTTP requests within milliseconds, flooding both the client's network stack and the backend servers.
2. **Severe Race Conditions**: Network requests do not guarantee First-In-First-Out (FIFO) arrival. An earlier request with slow latency can finish after a newer, faster request, causing obsolete data to overwrite the latest search results.
3. **Server & Client Overload**: Backends must execute redundant database/search queries for partial prefixes, while the frontend continuously parses JSON and re-renders components unnecessarily.
4. **UI Jitter**: The UI rapidly flickers between loading and intermediate partial results.

Debouncing combined with request ID validation resolves these problems by waiting until user typing settles before initiating an API call, and discarding any out-of-order network responses.

---

## 5. How to Run

```bash
cd q4-react-search
npm install
npm run dev
```

The dev server will run on `http://localhost:5173`.

---

## 6. How to Test

```bash
cd q4-react-search
npm test
```

Runs 12 comprehensive unit tests using **Vitest** and **React Testing Library**:
- Controlled input rendering and typing.
- Verifying no immediate fetch on keystroke.
- Accurate 300ms debounce firing.
- Safe query parameter URL encoding.
- Loading indicator display.
- Rendering users list.
- "No users found." empty state.
- HTTP error handling.
- Out-of-order response rejection via Request IDs.
- State reset on clearing search.
- Debounce timer cleanup on re-render and unmount.
