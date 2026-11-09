import { useState, useEffect } from 'react';
import { fetchHealth, fetchReady, HealthResponse, ReadyResponse } from './api/client';

function App() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [ready, setReady] = useState<ReadyResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let mounted = true;
    
    async function loadHealth() {
      try {
        setLoading(true);
        setError(null);
        const data = await fetchHealth();
        if (mounted) {
          setHealth(data);
        }
      } catch (err) {
        if (mounted) {
          setError(err instanceof Error ? err.message : 'Failed to fetch health');
        }
      } finally {
        if (mounted) {
          setLoading(false);
        }
      }
    }

    async function loadReady() {
      try {
        const data = await fetchReady();
        if (mounted) {
          setReady(data);
        }
      } catch (err) {
        if (mounted) {
          setReady({ status: 'not-ready', timestamp: new Date().toISOString() });
        }
      }
    }

    loadHealth();
    loadReady();
    
    // Refresh every 30 seconds
    const interval = setInterval(() => {
      loadHealth();
      loadReady();
    }, 30000);
    
    return () => {
      mounted = false;
      clearInterval(interval);
    };
  }, []);

  if (loading && !health) {
    return (
      <div className="container">
        <header className="header">
          <h1>Cobalt Workbench</h1>
          <p className="subtitle">Alan Vo | AI & Machine Learning</p>
        </header>
        <div className="loading">
          <div className="spinner" />
          <span>Connecting to backend...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      <header className="header">
        <h1>Cobalt Workbench</h1>
        <p className="subtitle">Alan Vo | AI & Machine Learning</p>
      </header>

      <main>
        <section className="card">
          <h2 className="card-title">System Health</h2>
          
          {error && (
            <div className="error">
              <strong>Error:</strong> {error}
            </div>
          )}

          {health && (
            <div className="status-grid">
              <div className="status-item">
                <div className="status-label">Status</div>
                <div className={`status-value ${health.status === 'healthy' ? 'healthy' : 'unhealthy'}`}>
                  {health.status}
                </div>
              </div>
              <div className="status-item">
                <div className="status-label">Version</div>
                <div className="status-value">{health.version}</div>
              </div>
              <div className="status-item">
                <div className="status-label">Timestamp</div>
                <div className="status-value">{new Date(health.timestamp).toLocaleString()}</div>
              </div>
              <div className="status-item">
                <div className="status-label">Uptime</div>
                <div className="status-value">{formatUptime(health.uptime_seconds)}</div>
              </div>
              <div className="status-item">
                <div className="status-label">Environment</div>
                <div className="status-value">{health.environment}</div>
              </div>
            </div>
          )}
        </section>

        {ready && (
          <section className="card" style={{ marginTop: '1rem' }}>
            <h2 className="card-title">Readiness</h2>
            <div className="status-grid">
              <div className="status-item">
                <div className="status-label">Status</div>
                <div className={`status-value ${ready.status === 'ready' ? 'healthy' : 'unhealthy'}`}>
                  {ready.status}
                </div>
              </div>
              <div className="status-item">
                <div className="status-label">Checked</div>
                <div className="status-value">{new Date(ready.timestamp).toLocaleString()}</div>
              </div>
            </div>
          </section>
        )}

        <section className="card" style={{ marginTop: '1.5rem' }}>
          <h2 className="card-title">About</h2>
          <p style={{ color: '#444', lineHeight: 1.7 }}>
            Cobalt Workbench is a developer tool for scaling computer-use 2.0 with open-source
            drivers, cross-OS sandboxes, and benchmarks for training, evaluation, and data generation.
          </p>
          <ul style={{ marginTop: '1rem', paddingLeft: '1.5rem', color: '#444', lineHeight: 1.8 }}>
            <li>Cross-platform sandbox orchestration (lume VMs, Docker)</li>
            <li>Benchmark runner for agent evaluation</li>
            <li>Training data generation from recorded trajectories</li>
            <li>ARM64-native Docker images for Apple Silicon</li>
          </ul>
        </section>
      </main>

      <footer className="footer">
        <p>Cobalt Workbench © 2025 Alan Vo alanvo@gmail.com</p>
        <p>MIT Licensed | AI/ML Developer Tools</p>
      </footer>
    </div>
  );
}

function formatUptime(seconds: number): string {
  if (seconds < 60) return `${seconds.toFixed(1)}s`;
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ${Math.floor(seconds % 60)}s`;
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  return `${hours}h ${minutes}m`;
}

export default App;
