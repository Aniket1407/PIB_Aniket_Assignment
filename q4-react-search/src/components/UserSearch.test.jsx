import React from 'react';
import { render, screen, fireEvent, act, waitFor } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import UserSearch from './UserSearch';

describe('UserSearch Component', () => {
  beforeEach(() => {
    vi.useFakeTimers();
    global.fetch = vi.fn();
  });

  afterEach(() => {
    vi.useRealTimers();
    vi.restoreAllMocks();
  });

  it('1. renders search input properly', () => {
    render(<UserSearch />);
    const input = screen.getByPlaceholderText('Search users...');
    expect(input).toBeInTheDocument();
    expect(input.value).toBe('');
  });

  it('2. allows user to type into the input (controlled input)', () => {
    render(<UserSearch />);
    const input = screen.getByPlaceholderText('Search users...');
    fireEvent.change(input, { target: { value: 'john' } });
    expect(input.value).toBe('john');
  });

  it('3. does not call API immediately on keystroke', () => {
    render(<UserSearch />);
    const input = screen.getByPlaceholderText('Search users...');
    fireEvent.change(input, { target: { value: 'j' } });
    fireEvent.change(input, { target: { value: 'jo' } });
    fireEvent.change(input, { target: { value: 'joh' } });

    expect(global.fetch).not.toHaveBeenCalled();
  });

  it('4. calls API after the 300ms debounce delay has elapsed', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => [{ id: 1, name: 'John Doe', email: 'john@example.com' }],
    });

    render(<UserSearch />);
    const input = screen.getByPlaceholderText('Search users...');
    fireEvent.change(input, { target: { value: 'john' } });

    // Advance timers by 299ms - should still not be called
    act(() => {
      vi.advanceTimersByTime(299);
    });
    expect(global.fetch).not.toHaveBeenCalled();

    // Advance by 1ms to reach 300ms
    await act(async () => {
      vi.advanceTimersByTime(1);
    });

    expect(global.fetch).toHaveBeenCalledTimes(1);
    expect(global.fetch).toHaveBeenCalledWith('/api/users?search=john');
  });

  it('5. encodes query parameter correctly', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => [],
    });

    render(<UserSearch />);
    const input = screen.getByPlaceholderText('Search users...');
    fireEvent.change(input, { target: { value: 'john doe & co' } });

    await act(async () => {
      vi.advanceTimersByTime(300);
    });

    expect(global.fetch).toHaveBeenCalledWith('/api/users?search=john%20doe%20%26%20co');
  });

  it('6. displays loading state while request is pending', async () => {
    // Hang the fetch promise to inspect loading state
    let resolvePromise;
    global.fetch.mockReturnValueOnce(
      new Promise((resolve) => {
        resolvePromise = resolve;
      })
    );

    render(<UserSearch />);
    const input = screen.getByPlaceholderText('Search users...');
    fireEvent.change(input, { target: { value: 'jane' } });

    act(() => {
      vi.advanceTimersByTime(300);
    });

    expect(screen.getByText('Searching...')).toBeInTheDocument();

    // Clean up pending promise
    await act(async () => {
      resolvePromise({
        ok: true,
        json: async () => [],
      });
    });
  });

  it('7. displays successful user search results', async () => {
    const mockUsers = [
      { id: 1, name: 'John Doe', email: 'john@example.com' },
      { id: 2, name: 'Jane Doe', email: 'jane@example.com' },
    ];

    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockUsers,
    });

    render(<UserSearch />);
    const input = screen.getByPlaceholderText('Search users...');
    fireEvent.change(input, { target: { value: 'doe' } });

    await act(async () => {
      await vi.advanceTimersByTimeAsync(300);
    });

    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('john@example.com')).toBeInTheDocument();
    expect(screen.getByText('Jane Doe')).toBeInTheDocument();
    expect(screen.getByText('jane@example.com')).toBeInTheDocument();
    expect(screen.queryByText('Searching...')).not.toBeInTheDocument();
  });

  it('8. displays "No users found." when search returns empty array', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => [],
    });

    render(<UserSearch />);
    const input = screen.getByPlaceholderText('Search users...');
    fireEvent.change(input, { target: { value: 'nonexistent' } });

    await act(async () => {
      await vi.advanceTimersByTimeAsync(300);
    });

    expect(screen.getByText('No users found.')).toBeInTheDocument();
  });

  it('9. displays user-friendly error on HTTP / network failure', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: false,
      status: 500,
    });

    render(<UserSearch />);
    const input = screen.getByPlaceholderText('Search users...');
    fireEvent.change(input, { target: { value: 'errorQuery' } });

    await act(async () => {
      await vi.advanceTimersByTimeAsync(300);
    });

    expect(screen.getByText('Something went wrong. Please try again.')).toBeInTheDocument();
    expect(screen.queryByText('Searching...')).not.toBeInTheDocument();
  });


  it('10. ignores stale / out-of-order responses using request ID mechanism', async () => {
    let resolveFirstRequest;
    let resolveSecondRequest;

    // First request ("jo") starts and takes longer
    global.fetch.mockReturnValueOnce(
      new Promise((resolve) => {
        resolveFirstRequest = resolve;
      })
    );

    // Second request ("john") starts after user types more
    global.fetch.mockReturnValueOnce(
      new Promise((resolve) => {
        resolveSecondRequest = resolve;
      })
    );

    render(<UserSearch />);
    const input = screen.getByPlaceholderText('Search users...');

    // User types "jo"
    fireEvent.change(input, { target: { value: 'jo' } });
    act(() => {
      vi.advanceTimersByTime(300);
    });
    expect(global.fetch).toHaveBeenCalledWith('/api/users?search=jo');

    // User types "john" before "jo" completes
    fireEvent.change(input, { target: { value: 'john' } });
    act(() => {
      vi.advanceTimersByTime(300);
    });
    expect(global.fetch).toHaveBeenCalledWith('/api/users?search=john');

    // Second request ("john") finishes first!
    await act(async () => {
      resolveSecondRequest({
        ok: true,
        json: async () => [{ id: 10, name: 'John Result', email: 'john@new.com' }],
      });
    });

    expect(screen.getByText('John Result')).toBeInTheDocument();

    // First request ("jo") finishes afterward (stale!)
    await act(async () => {
      resolveFirstRequest({
        ok: true,
        json: async () => [{ id: 20, name: 'Jo Old Result', email: 'jo@old.com' }],
      });
    });

    // Verify "Jo Old Result" was completely ignored and "John Result" remains visible
    expect(screen.queryByText('Jo Old Result')).not.toBeInTheDocument();
    expect(screen.getByText('John Result')).toBeInTheDocument();
  });

  it('11. clearing search does not trigger API call and resets state', async () => {
    render(<UserSearch />);
    const input = screen.getByPlaceholderText('Search users...');

    // Type and then immediately clear
    fireEvent.change(input, { target: { value: 'test' } });
    fireEvent.change(input, { target: { value: '' } });

    await act(async () => {
      vi.advanceTimersByTime(350);
    });

    expect(global.fetch).not.toHaveBeenCalled();
    expect(screen.queryByText('Searching...')).not.toBeInTheDocument();
    expect(screen.queryByText('No users found.')).not.toBeInTheDocument();
  });

  it('12. cleans up debounce timer when input changes or component unmounts', () => {
    const clearTimeoutSpy = vi.spyOn(global, 'clearTimeout');
    const { unmount } = render(<UserSearch />);
    const input = screen.getByPlaceholderText('Search users...');

    fireEvent.change(input, { target: { value: 'typing' } });
    fireEvent.change(input, { target: { value: 'typing more' } });

    expect(clearTimeoutSpy).toHaveBeenCalled();

    unmount();
    expect(clearTimeoutSpy).toHaveBeenCalled();
  });
});
