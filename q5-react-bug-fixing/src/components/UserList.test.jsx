import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import UserList from './UserList';

describe('UserList Component Bug Fixes & Behavior', () => {
  const sampleUsers = [
    { id: 1, name: 'Alice Smith' },
    { id: 2, name: 'Bob Jones' },
    { id: 3, name: 'Charlie Brown' },
  ];

  it('1. renders all users passed via props', () => {
    render(<UserList users={sampleUsers} />);
    expect(screen.getByText('Alice Smith')).toBeInTheDocument();
    expect(screen.getByText('Bob Jones')).toBeInTheDocument();
    expect(screen.getByText('Charlie Brown')).toBeInTheDocument();
  });

  it('2. each rendered user uses a stable id for identification without key warnings', () => {
    const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
    render(<UserList users={sampleUsers} />);
    // Verify no React key warnings were emitted
    expect(consoleErrorSpy).not.toHaveBeenCalledWith(
      expect.stringContaining('Each child in a list should have a unique "key" prop')
    );
    consoleErrorSpy.mockRestore();
  });

  it('3. initially displays no selected user ("None")', () => {
    render(<UserList users={sampleUsers} />);
    const display = screen.getByTestId('selected-user-display');
    expect(display).toHaveTextContent('None');
  });

  it('4. selecting a user displays their information', () => {
    render(<UserList users={sampleUsers} />);
    const aliceBtn = screen.getByTestId('user-item-1');
    fireEvent.click(aliceBtn);

    const display = screen.getByTestId('selected-user-display');
    expect(display).toHaveTextContent('Alice Smith (ID: 1)');
  });

  it('5. selecting another user updates the displayed details', () => {
    render(<UserList users={sampleUsers} />);
    const aliceBtn = screen.getByTestId('user-item-1');
    const bobBtn = screen.getByTestId('user-item-2');

    fireEvent.click(aliceBtn);
    expect(screen.getByTestId('selected-user-display')).toHaveTextContent('Alice Smith (ID: 1)');

    fireEvent.click(bobBtn);
    expect(screen.getByTestId('selected-user-display')).toHaveTextContent('Bob Jones (ID: 2)');
  });

  it('6. clear button resets the selection', () => {
    render(<UserList users={sampleUsers} />);
    fireEvent.click(screen.getByTestId('user-item-2'));
    expect(screen.getByTestId('selected-user-display')).toHaveTextContent('Bob Jones (ID: 2)');

    fireEvent.click(screen.getByTestId('clear-selection-btn'));
    expect(screen.getByTestId('selected-user-display')).toHaveTextContent('None');
  });

  it('7. derived state prevents stale user object when user prop updates', () => {
    const { rerender } = render(<UserList users={sampleUsers} />);
    // Select user 1 ("Alice Smith")
    fireEvent.click(screen.getByTestId('user-item-1'));
    expect(screen.getByTestId('selected-user-display')).toHaveTextContent('Alice Smith (ID: 1)');

    // Parent updates Alice's name in the users array
    const updatedUsers = [
      { id: 1, name: 'Alice Wonder' },
      { id: 2, name: 'Bob Jones' },
    ];
    rerender(<UserList users={updatedUsers} />);

    // Since selectedUser is derived from users + selectedUserId, it reflects the updated name immediately!
    expect(screen.getByTestId('selected-user-display')).toHaveTextContent('Alice Wonder (ID: 1)');
    expect(screen.queryByText('Alice Smith')).not.toBeInTheDocument();
  });

  it('8. removing the selected user safely resets selection to None', () => {
    const { rerender } = render(<UserList users={sampleUsers} />);
    // Select user 2 ("Bob Jones")
    fireEvent.click(screen.getByTestId('user-item-2'));
    expect(screen.getByTestId('selected-user-display')).toHaveTextContent('Bob Jones (ID: 2)');

    // Re-render with Bob removed from users
    const usersWithoutBob = [
      { id: 1, name: 'Alice Smith' },
      { id: 3, name: 'Charlie Brown' },
    ];
    rerender(<UserList users={usersWithoutBob} />);

    // The display must not show Bob anymore!
    expect(screen.getByTestId('selected-user-display')).toHaveTextContent('None');
    expect(screen.queryByText('Bob Jones')).not.toBeInTheDocument();
  });

  it('9. component does not enter an infinite render loop', () => {
    let renderCount = 0;
    function Wrapper() {
      renderCount++;
      return <UserList users={sampleUsers} />;
    }

    render(<Wrapper />);
    // Initial mount renders once or twice (React StrictMode), but must stabilize and not run infinitely
    expect(renderCount).toBeLessThan(5);
  });

  it('10. does not mutate the original input users array', () => {
    const original = [
      { id: 1, name: 'A' },
      { id: 2, name: 'B' },
    ];
    const copy = JSON.parse(JSON.stringify(original));
    render(<UserList users={original} />);
    fireEvent.click(screen.getByTestId('user-item-1'));
    fireEvent.click(screen.getByTestId('clear-selection-btn'));

    expect(original).toEqual(copy);
  });

  it('11. handles empty or undefined users prop safely', () => {
    render(<UserList users={[]} />);
    expect(screen.getByTestId('selected-user-display')).toHaveTextContent('None');
  });
});
