export interface HealthResponse {
  status: string;
  version: string;
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