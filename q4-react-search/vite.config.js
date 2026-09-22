import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// Mock users database for screen testing
const MOCK_USERS = [
  { id: 1, name: 'Amit Sharma',     email: 'amit.sharma@example.com' },
  { id: 2, name: 'Ananya Singh',    email: 'ananya.singh@example.com' },
  { id: 3, name: 'Rahul Verma',     email: 'rahul.verma@example.com' },
  { id: 4, name: 'Priya Patel',     email: 'priya.patel@example.com' },
  { id: 5, name: 'Sneha Reddy',     email: 'sneha.reddy@example.com' },
  { id: 6, name: 'Rohan Joshi',     email: 'rohan.joshi@example.com' },
  { id: 7, name: 'Meera Iyer',      email: 'meera.iyer@example.com' },
  { id: 8, name: 'Arjun Kapoor',    email: 'arjun.kapoor@example.com' },
  { id: 9, name: 'Divya Deshmukh', email: 'divya.deshmukh@example.com' },
  { id: 10, name: 'Aniket Gautam', email: 'aniket.gautam@example.com' },
];

// Vite plugin: mock /api/users?search=<query>
function mockApiPlugin() {
  return {
    name: 'mock-api',
    configureServer(server) {
      server.middlewares.use('/api/users', (req, res) => {
        const url = new URL(req.url, 'http://localhost');
        const query = (url.searchParams.get('search') || '').toLowerCase().trim();
        const results = query
          ? MOCK_USERS.filter(
              (u) =>
                u.name.toLowerCase().includes(query) ||
                u.email.toLowerCase().includes(query)
            )
          : [];
        res.setHeader('Content-Type', 'application/json');
        res.end(JSON.stringify(results));
      });
    },
  };
}

export default defineConfig({
  plugins: [react(), mockApiPlugin()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: './src/test-setup.js',
  },
});
