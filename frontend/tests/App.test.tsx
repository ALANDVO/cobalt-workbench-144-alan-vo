import { describe, it, expect, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import App from '../src/App';
import { fetchHealth, HealthResponse } from '../src/api/client';

vi.mock('../src/api/client', () => ({
  fetchHealth: vi.fn(),
}));

const mockFetchHealth = vi.mocked(fetchHealth);

describe('App', () => {
  beforeEach(() => {
    vi.resetAllMocks();
  });

  it('shows loading state initially', () => {
    const { promise, resolve } = Promise.withResolvers<HealthResponse>();
    mockFetchHealth.mockReturnValue(promise);
    render(<App />);
    expect(screen.getByText('Connecting to backend...')).toBeInTheDocument();
    resolve({ status: 'healthy', version: '1.0.0', timestamp: '2025-01-15T10:30:00Z' });
  });

  it('displays health data when fetch succeeds', async () => {
    const mockHealth: HealthResponse = {
      status: 'healthy',
      version: '1.0.0',
      timestamp: '2025-01-15T10:30:00Z',
    };
    mockFetchHealth.mockResolvedValue(mockHealth);
    
    render(<App />);
    
    await waitFor(() => {
      expect(screen.getByText('System Health')).toBeInTheDocument();
    });
    
    expect(screen.getByText('healthy')).toBeInTheDocument();
    expect(screen.getByText('1.0.0')).toBeInTheDocument();
  });

  it('displays error when fetch fails', async () => {
    mockFetchHealth.mockRejectedValue(new Error('Connection refused'));
    
    render(<App />);
    
    await waitFor(() => {
      expect(screen.getByText(/Error:/)).toBeInTheDocument();
      expect(screen.getByText('Connection refused')).toBeInTheDocument();
    });
  });
});