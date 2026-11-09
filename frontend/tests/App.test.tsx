import { describe, it, expect, vi } from 'vitest';
import { render, screen, waitFor, act } from '@testing-library/react';
import App from '../src/App';
import { fetchHealth, fetchReady, HealthResponse, ReadyResponse } from '../src/api/client';

vi.mock('../src/api/client', () => ({
  fetchHealth: vi.fn(),
  fetchReady: vi.fn(),
}));

const mockFetchHealth = vi.mocked(fetchHealth);
const mockFetchReady = vi.mocked(fetchReady);

describe('App', () => {
  beforeEach(() => {
    vi.resetAllMocks();
  });

  const mockHealth: HealthResponse = {
    status: 'healthy',
    version: '1.0.0',
    timestamp: '2025-01-15T10:30:00Z',
    uptime_seconds: 123.45,
    environment: 'development',
  };

  const mockReady: ReadyResponse = {
    status: 'ready',
    timestamp: '2025-01-15T10:30:00Z',
  };

  it('shows loading state initially', async () => {
    const { promise, resolve } = Promise.withResolvers<HealthResponse>();
    mockFetchHealth.mockReturnValue(promise);
    mockFetchReady.mockResolvedValue(mockReady);
    
    await act(async () => {
      render(<App />);
      await Promise.resolve();
    });
    
    expect(screen.getByText('Connecting to backend...')).toBeInTheDocument();
    
    await act(async () => {
      resolve(mockHealth);
      await promise;
    });
  });

  it('displays health data when fetch succeeds', async () => {
    mockFetchHealth.mockResolvedValue(mockHealth);
    mockFetchReady.mockResolvedValue(mockReady);
    
    await act(async () => {
      render(<App />);
      await Promise.resolve();
    });
    
    await waitFor(() => {
      expect(screen.getByText('System Health')).toBeInTheDocument();
    });
    
    expect(screen.getByText('healthy')).toBeInTheDocument();
    expect(screen.getByText('1.0.0')).toBeInTheDocument();
    expect(screen.getByText('development')).toBeInTheDocument();
    expect(screen.getByText('2m 3s')).toBeInTheDocument(); // uptime format
  });

  it('displays readiness data when fetch succeeds', async () => {
    mockFetchHealth.mockResolvedValue(mockHealth);
    mockFetchReady.mockResolvedValue(mockReady);
    
    await act(async () => {
      render(<App />);
      await Promise.resolve();
    });
    
    await waitFor(() => {
      expect(screen.getByText('Readiness')).toBeInTheDocument();
    });
    
    expect(screen.getByText('ready')).toBeInTheDocument();
  });

  it('displays error when health fetch fails', async () => {
    mockFetchHealth.mockRejectedValue(new Error('Connection refused'));
    mockFetchReady.mockResolvedValue(mockReady);
    
    await act(async () => {
      render(<App />);
      await Promise.resolve();
    });
    
    await waitFor(() => {
      expect(screen.getByText(/Error:/)).toBeInTheDocument();
      expect(screen.getByText('Connection refused')).toBeInTheDocument();
    });
  });

  it('displays not-ready when readiness fetch fails', async () => {
    mockFetchHealth.mockResolvedValue(mockHealth);
    mockFetchReady.mockRejectedValue(new Error('Service unavailable'));
    
    await act(async () => {
      render(<App />);
      await Promise.resolve();
    });
    
    await waitFor(() => {
      expect(screen.getByText('Readiness')).toBeInTheDocument();
    });
    
    expect(screen.getByText('not-ready')).toBeInTheDocument();
  });
});
