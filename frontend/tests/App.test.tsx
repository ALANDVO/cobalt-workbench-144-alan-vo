import { describe, it, expect, vi } from 'vitest';
import { render, screen, waitFor, act } from '@testing-library/react';
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

  it('shows loading state initially', async () => {
    const { promise, resolve } = Promise.withResolvers<HealthResponse>();
    mockFetchHealth.mockReturnValue(promise);
    
    await act(async () => {
      render(<App />);
      await Promise.resolve();
    });
    
    expect(screen.getByText('Connecting to backend...')).toBeInTheDocument();
    
    await act(async () => {
      resolve({ status: 'healthy', version: '1.0.0', timestamp: '2025-01-15T10:30:00Z' });
      await promise;
    });
  });

  it('displays health data when fetch succeeds', async () => {
    const mockHealth: HealthResponse = {
      status: 'healthy',
      version: '1.0.0',
      timestamp: '2025-01-15T10:30:00Z',
    };
    mockFetchHealth.mockResolvedValue(mockHealth);
    
    await act(async () => {
      render(<App />);
      await Promise.resolve();
    });
    
    await waitFor(() => {
      expect(screen.getByText('System Health')).toBeInTheDocument();
    });
    
    expect(screen.getByText('healthy')).toBeInTheDocument();
    expect(screen.getByText('1.0.0')).toBeInTheDocument();
  });

  it('displays error when fetch fails', async () => {
    mockFetchHealth.mockRejectedValue(new Error('Connection refused'));
    
    await act(async () => {
      render(<App />);
      await Promise.resolve();
    });
    
    await waitFor(() => {
      expect(screen.getByText(/Error:/)).toBeInTheDocument();
      expect(screen.getByText('Connection refused')).toBeInTheDocument();
    });
  });
});
