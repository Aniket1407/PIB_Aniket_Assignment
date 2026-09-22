import React, { useState } from 'react';
import UserList from './components/UserList';

const INITIAL_USERS = [
  { id: 1, name: 'Rahul Sharma' },
  { id: 2, name: 'Priya Patel' },
  { id: 3, name: 'Amit Singh' },
];

export default function App() {
  const [users, setUsers] = useState(INITIAL_USERS);
  const [selectedUserId, setSelectedUserId] = useState(null);

  const selectedUser = users.find((u) => u.id === selectedUserId) ?? null;

  const handleRemoveSelected = () => {
    if (selectedUserId !== null) {
      setUsers((prev) => prev.filter((u) => u.id !== selectedUserId));
      setSelectedUserId(null);
    }
  };

  const handleReset = () => {
    setUsers(INITIAL_USERS);
    setSelectedUserId(null);
  };

  return (
    <main style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
      <UserList
        users={users}
        selectedUserId={selectedUserId}
        onSelectUser={setSelectedUserId}
      />
      <div
        style={{
          maxWidth: '400px',
          margin: '1.5rem auto',
          display: 'flex',
          flexDirection: 'column',
          gap: '0.75rem',
        }}
      >
        <button
          type="button"
          onClick={handleRemoveSelected}
          disabled={!selectedUser}
          style={{
            padding: '0.65rem 1rem',
            fontSize: '0.95rem',
            backgroundColor: selectedUser ? '#dc3545' : '#e9ecef',
            color: selectedUser ? '#ffffff' : '#6c757d',
            border: selectedUser ? '1px solid #dc3545' : '1px solid #ced4da',
            borderRadius: '4px',
            cursor: selectedUser ? 'pointer' : 'not-allowed',
            fontWeight: '600',
            transition: 'all 0.2s ease',
          }}
        >
          {selectedUser
            ? `Remove ${selectedUser.name} (ID: ${selectedUser.id})`
            : 'Select a user above to remove'}
        </button>

        <button
          type="button"
          onClick={handleReset}
          style={{
            padding: '0.5rem 0.8rem',
            fontSize: '0.9rem',
            backgroundColor: '#f8f9fa',
            border: '1px solid #ccc',
            borderRadius: '4px',
            cursor: 'pointer',
          }}
        >
          Reset Users
        </button>
      </div>
    </main>
  );
}
