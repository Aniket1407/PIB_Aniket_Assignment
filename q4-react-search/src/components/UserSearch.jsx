import React, { useState, useEffect, useRef } from 'react';

const DEBOUNCE_DELAY = 300;

export default function UserSearch() {
  const [search, setSearch] = useState('');
  const [debouncedSearch, setDebouncedSearch] = useState('');
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Request counter to guard against race conditions / stale responses
  const latestRequestIdRef = useRef(0);

  // 1. Debounce Effect: Update debouncedSearch after DEBOUNCE_DELAY ms of inactivity
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedSearch(search);
    }, DEBOUNCE_DELAY);

    return () => {
      clearTimeout(timer);
    };
  }, [search]);

  // 2. Search Effect: Trigger network request whenever debouncedSearch updates
  useEffect(() => {
    const trimmedQuery = debouncedSearch.trim();

    // When query is empty, do not call API; clear states
    if (!trimmedQuery) {
      setUsers([]);
      setError(null);
      setLoading(false);
      return;
    }

    const currentRequestId = ++latestRequestIdRef.current;
    setLoading(true);
    setError(null);

    const fetchUsers = async () => {
      try {
        const encodedQuery = encodeURIComponent(trimmedQuery);
        const response = await fetch(`/api/users?search=${encodedQuery}`);

        // If a newer request has started since this request was initiated, ignore response
        if (currentRequestId !== latestRequestIdRef.current) {
          return;
        }

        if (!response.ok) {
          throw new Error(`Server returned HTTP ${response.status}`);
        }

        const data = await response.json();

        // Check again after JSON parsing
        if (currentRequestId !== latestRequestIdRef.current) {
          return;
        }

        setUsers(Array.isArray(data) ? data : []);
        setLoading(false);
      } catch (err) {
        // Only update UI with error if this is still the latest active request
        if (currentRequestId === latestRequestIdRef.current) {
          setError('Something went wrong. Please try again.');
          setUsers([]);
          setLoading(false);
        }
      }
    };

    fetchUsers();
  }, [debouncedSearch]);

  const hasSearched = Boolean(debouncedSearch.trim());

  return (
    <div style={{ maxWidth: '500px', margin: '2rem auto', fontFamily: 'sans-serif' }}>
      <h2>User Search</h2>
      <div style={{ marginBottom: '1rem' }}>
        <input
          type="text"
          placeholder="Search users..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{
            width: '100%',
            padding: '0.6rem 0.8rem',
            fontSize: '1rem',
            borderRadius: '4px',
            border: '1px solid #ccc',
            boxSizing: 'border-box',
          }}
        />
      </div>

      {loading && <div style={{ color: '#555', fontStyle: 'italic' }}>Searching...</div>}

      {!loading && error && (
        <div style={{ color: '#d9534f', padding: '0.5rem 0' }}>{error}</div>
      )}

      {!loading && !error && hasSearched && users.length === 0 && (
        <div style={{ color: '#777' }}>No users found.</div>
      )}

      {!loading && !error && users.length > 0 && (
        <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
          {users.map((user) => (
            <li
              key={user.id}
              style={{
                padding: '0.6rem 0.8rem',
                borderBottom: '1px solid #eee',
                display: 'flex',
                justifyContent: 'space-between',
              }}
            >
              <strong>{user.name}</strong>
              <span style={{ color: '#666' }}>{user.email}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
