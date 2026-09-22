import React, { useState, useEffect } from 'react';

export default function UserList({
  users = [],
  selectedUserId: externalSelectedUserId,
  onSelectUser,
}) {
  // Store only the primitive selected user ID instead of the entire user object.
  // This avoids storing stale object copies and maintains a single source of truth.
  const [internalSelectedId, setInternalSelectedId] = useState(null);

  const isControlled = externalSelectedUserId !== undefined;
  const selectedUserId = isControlled ? externalSelectedUserId : internalSelectedId;

  // Derive the selected user directly from the users prop during rendering.
  const selectedUser = users.find((user) => user.id === selectedUserId) ?? null;

  const handleSelect = (id) => {
    if (!isControlled) {
      setInternalSelectedId(id);
    }
    onSelectUser?.(id);
  };

  const handleClear = () => {
    if (!isControlled) {
      setInternalSelectedId(null);
    }
    onSelectUser?.(null);
  };

  // Synchronization effect: If the currently selected user is removed from the users prop,
  // reset selectedUserId to null so the component does not retain an orphaned ID.
  useEffect(() => {
    if (selectedUserId !== null && !users.some((u) => u.id === selectedUserId)) {
      if (!isControlled) {
        setInternalSelectedId(null);
      }
      onSelectUser?.(null);
    }
  }, [users, selectedUserId, isControlled, onSelectUser]);

  // Log selection updates with proper dependency array (avoids running on every render)
  useEffect(() => {
    if (selectedUser) {
      console.log('Selected:', selectedUser);
    }
  }, [selectedUser]);

  return (
    <div style={{ maxWidth: '400px', margin: '2rem auto', fontFamily: 'sans-serif' }}>
      <h3>User Directory</h3>
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {users.map((user) => (
          <li key={user.id} style={{ marginBottom: '0.5rem' }}>
            <button
              type="button"
              data-testid={`user-item-${user.id}`}
              onClick={() => handleSelect(user.id)}
              style={{
                width: '100%',
                textAlign: 'left',
                padding: '0.6rem 0.8rem',
                border: selectedUserId === user.id ? '2px solid #0066cc' : '1px solid #ccc',
                backgroundColor: selectedUserId === user.id ? '#e6f0ff' : '#fff',
                borderRadius: '4px',
                cursor: 'pointer',
                fontWeight: selectedUserId === user.id ? 'bold' : 'normal',
              }}
            >
              {user.name}
            </button>
          </li>
        ))}
      </ul>

      <div style={{ margin: '1rem 0' }}>
        <button
          type="button"
          data-testid="clear-selection-btn"
          onClick={handleClear}
          style={{
            padding: '0.5rem 1rem',
            backgroundColor: '#f5f5f5',
            border: '1px solid #ccc',
            borderRadius: '4px',
            cursor: 'pointer',
          }}
        >
          Clear
        </button>
      </div>

      <div
        data-testid="selected-user-display"
        style={{
          padding: '0.8rem',
          backgroundColor: '#fafafa',
          border: '1px solid #eee',
          borderRadius: '4px',
        }}
      >
        <strong>Selected: </strong>
        {selectedUser ? (
          <span>{selectedUser.name} (ID: {selectedUser.id})</span>
        ) : (
          <span style={{ color: '#888' }}>None</span>
        )}
      </div>
    </div>
  );
}
