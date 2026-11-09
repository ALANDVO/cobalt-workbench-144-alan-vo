export interface HealthResponse {
  status: string;
  version: string;
  timestamp: string;
  uptime_seconds: number;
  environment: string;
}

export interface ReadyResponse {
  status: string;
  timestamp: string;
}

const API_BASE = '/api/v1';

export async function fetchHealth(): Promise<HealthResponse> {
  const response = await fetch(`${API_BASE}/health`);
  if (!response.ok) {
    throw new Error(`Health check failed: ${response.status}`);
  }
  return response.json();
}

export async function fetchReady(): Promise<ReadyResponse> {
  const response = await fetch(`${API_BASE}/ready`);
  if (!response.ok) {
    throw new Error(`Readiness check failed: ${response.status}`);
  }
  return response.json();
}

const API_BASE = '/api/v1';

export async function fetchHealth(): Promise<HealthResponse> {
  const response = await fetch(`${API_BASE}/health`);
  if (!response.ok) {
    throw new Error(`Health check failed: ${response.status}`);
  }
  return response.json();
}