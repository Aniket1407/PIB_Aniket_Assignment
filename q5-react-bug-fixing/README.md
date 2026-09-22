# Question 5: React Bug Fixing

A corrected, interview-ready implementation of the `UserList` component located under `q5-react-bug-fixing/src/components/UserList.jsx`.

---

## 1. Original Assessment Code
```jsx
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
      <button onClick={() => setSelectedUser(null)}>
        Clear
      </button>
    </div>
  );
}
```

---

## 2. Genuine Problems Found & Why They Are Problematic

### Problem 1: Missing `key` prop on mapped list items
- **What was wrong**: `{users.map((user) => (<div onClick=...>{user.name}</div>))}` did not provide a `key` prop.
- **Why it matters**: React uses keys to match virtual DOM nodes with actual DOM elements during reconciliation. Without stable keys, React logs a console error and falls back to array index matching, which causes rendering inefficiencies and can lead to incorrect state retention when items are reordered, inserted, or removed.
- **Fix**: Added unique stable `key={user.id}`.

### Problem 2: Missing Dependency Array in `useEffect`
- **What was wrong**: `useEffect(() => { console.log(...); });` has no dependency array.
- **Why it matters**: Without a dependency array, the effect executes after **every single render** (every time parent re-renders, any state changes, or any prop updates). If an effect contains state setters, this causes an infinite render loop. Even for side effects, it causes unnecessary execution overhead.
- **Fix**: Added explicit dependency array `[selectedUser]` (or `[selectedUserId]`).

### Problem 3: Storing Full Object in State (`selectedUser`) Leading to Stale State
- **What was wrong**: `const [selectedUser, setSelectedUser] = useState(null)` duplicated complete user objects from `props.users`.
- **Why it matters**:
  1. If the parent updates user data in the `users` prop (e.g. name update from "Alice" to "Alice Smith"), `selectedUser` in state retains the old, stale snapshot object.
  2. If the selected user is deleted/removed from `users`, `selectedUser` continues holding on to the deleted user.
- **Fix**: Store only the primitive `selectedUserId`:
  ```javascript
  const [selectedUserId, setSelectedUserId] = useState(null);
  ```
  And derive `selectedUser` directly during render:
  ```javascript
  const selectedUser = users.find(u => u.id === selectedUserId) ?? null;
  ```
  This guarantees that data is always read from the single source of truth (`props.users`).

### Problem 4: Missing Selected User Display
- **What was wrong**: The original component allowed selecting a user, but never actually displayed the selected user's details anywhere in the UI.
- **Fix**: Rendered a dedicated status section showing the currently selected user's name and ID, or "None" when no user is selected.

### Problem 5: Non-Semantic & Inaccessible Interactive Elements
- **What was wrong**: Plain `<div>` elements with `onClick` were used for user selection, lacking keyboard accessibility (`Enter`/`Space`) and proper button semantics.
- **Fix**: Replaced with `<button type="button">` inside a semantic `<ul>` / `<li>` list structure.

### Problem 6: Potential Crash on Undefined `users` Prop
- **What was wrong**: If `users` is `undefined` or `null`, `users.map()` throws a TypeError.
- **Fix**: Added default parameter `users = []`.

---

## 3. Selected User ID vs Storing Complete Object
- **Single Source of Truth**: Props are the authoritative source of user data. Duplicating objects into local state creates multiple conflicting sources of truth.
- **Zero Synchronization Overhead**: By deriving `selectedUser = users.find(...)` during render, any change in parent data (name updates, email updates, status changes) automatically reflects in the selected user view without extra effects or manual syncing.

---

## 4. Handling Invalid Selections (User Removal)
When `users` prop changes and the selected user is no longer in the list:
1. `selectedUser` immediately evaluates to `null` during render, preventing stale display.
2. A lightweight synchronization effect clears the orphaned ID:
   ```javascript
   useEffect(() => {
     if (selectedUserId !== null && !users.some(u => u.id === selectedUserId)) {
       setSelectedUserId(null);
     }
   }, [users, selectedUserId]);
   ```

---

## 5. How to Run

```bash
cd q5-react-bug-fixing
npm install
npm run dev
```

Runs on `http://localhost:5173`.

---

## 6. How to Test

```bash
cd q5-react-bug-fixing
npm test
```

11 automated tests using **Vitest** and **React Testing Library** verify:
1. Rendering all users.
2. Stable `key` usage with zero React warnings.
3. Initial "None" selection display.
4. User selection update.
5. Switching between different users.
6. Clear selection button.
7. Fresh data reflection without stale objects when props change.
8. Safe selection reset when the selected user is removed.
9. No infinite render loops.
10. Input prop immutability.
11. Safe handling of empty arrays.
