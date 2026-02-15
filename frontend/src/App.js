import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

let BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:3000/api/v1/task';

// Robustness: Ensure protocol and path
if (BACKEND_URL && !BACKEND_URL.startsWith('http')) {
    // If it looks like a hostname (no slashes), add https
    if (!BACKEND_URL.includes('/')) {
        BACKEND_URL = `https://${BACKEND_URL}.onrender.com/api/v1/task`;
    } else {
        BACKEND_URL = `https://${BACKEND_URL}`;
    }
}
if (BACKEND_URL && !BACKEND_URL.endsWith('/api/v1/task')) {
    BACKEND_URL = `${BACKEND_URL.replace(/\/$/, '')}/api/v1/task`;
}

console.log('🌐 Using Backend URL:', BACKEND_URL);

const DEMO_DATA = {
    'Live Editor': { title: '', desc: '', github: '', demo: false, type: null },
    'Good Submission': {
        title: 'Enterprise-Grade Distributed Task Processing System with Resilience and Monitoring',
        desc: 'Objective: To architect and implement a horizontally scalable task processing engine. Requirements include high availability via multi-node deployments, failure resilience using exponential backoff with dead-letter queues, and real-time observability. The goal is to ensure 99.9% uptime by utilizing production-grade monitoring suites like Prometheus and Grafana. This requirement covers security constraints for mTLS and internal authentication. The purpose is to handle high-throughput workloads with sub-50ms latency while maintaining full database consistency across shards. Performance optimization is achieved through efficient connection pooling and asynchronous execution patterns. Final success criteria: 100% test coverage and full audit logging.',
        github: 'https://github.com/fastapi/fastapi',
        demo: true,
        type: 'good'
    },
    'Partial Submission': {
        title: 'Standard API Implementation for Basic Data Operations and Storage',
        desc: 'Requirement: The objective is to build an API that connects to a SQL database. It should handle GET and POST requests for user data. Some security constraints like basic auth should be added eventually. The purpose is to make the system work for the initial release. We need to handle basic database connections and ensure some error handling is present in the main controller.',
        github: 'https://github.com/encode/uvicorn',
        demo: true,
        type: 'partial'
    },
    'Poor Submission': {
        title: 'Fix fast',
        desc: 'fix the bugs in the code quickly. make it run without error. just get it done today.',
        github: '',
        demo: true,
        type: 'poor'
    }
};

function App() {
    const [scenario, setScenario] = useState('Live Editor');
    const [taskTitle, setTaskTitle] = useState('');
    const [taskDesc, setTaskDesc] = useState('');
    const [submittedBy, setSubmittedBy] = useState('Demo Professional');
    const [githubUrl, setGithubUrl] = useState('');
    const [pdfFile, setPdfFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);
    const [backendStatus, setBackendStatus] = useState('checking');
    const [theme, setTheme] = useState(localStorage.getItem('theme') || 'light');

    useEffect(() => {
        const current = DEMO_DATA[scenario];
        setTaskTitle(current.title);
        setTaskDesc(current.desc);
        setGithubUrl(current.github || '');
        setPdfFile(null);
        setResult(null);
        setError(null);
    }, [scenario]);

    useEffect(() => {
        checkBackendHealth();
    }, []);

    useEffect(() => {
        localStorage.setItem('theme', theme);
    }, [theme]);

    const toggleTheme = () => {
        setTheme(prev => prev === 'light' ? 'dark' : 'light');
    };

    const checkBackendHealth = async () => {
        try {
            const healthUrl = BACKEND_URL.replace('/api/v1/task', '/health');
            const response = await axios.get(healthUrl, { timeout: 5000 });
            if (response.status === 200) {
                setBackendStatus('online');
            }
        } catch (err) {
            setBackendStatus('offline');
        }
    };

    const handleFileChange = (e) => {
        if (e.target.files && e.target.files[0]) {
            setPdfFile(e.target.files[0]);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        setResult(null);

        const formData = new FormData();
        if (taskTitle) formData.append('title', taskTitle); // Title is used for display in orchestrator
        if (taskDesc) formData.append('description', taskDesc);
        if (githubUrl) formData.append('github_url', githubUrl);
        if (pdfFile) formData.append('pdf_file', pdfFile);
        formData.append('submitted_by', submittedBy);

        try {
            // Unified Orchestration Call
            const response = await axios.post(`${BACKEND_URL}/review`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });

            const reviewData = response.data;
            const nextTaskData = reviewData.next_task || {
                title: 'Proceed to Next Step',
                objective: 'General follow-up.',
                difficulty: 'medium'
            };

            setResult({ review: reviewData, nextTask: nextTaskData });
        } catch (err) {
            console.error('Submission Error:', err);
            const detail = err.response?.data?.detail;
            if (Array.isArray(detail)) {
                setError(detail.map(d => d.msg).join(', '));
            } else {
                setError(detail || err.message || 'An error occurred during analysis');
            }
        } finally {
            setLoading(false);
        }
    };

    const getStatusColor = (status) => {
        const colors = {
            pass: '#10b981',
            borderline: '#f59e0b',
            fail: '#ef4444'
        };
        return colors[status] || '#3b82f6';
    };

    const isDisabled = DEMO_DATA[scenario].demo;

    return (
        <div className={`App ${theme}`}>
            <div className="container">
                <header className="header">
                    <div className="header-content">
                        <h1 className="title">🛡️ Task Review AI</h1>
                        <p className="subtitle">Deterministic Engineering Task Analysis System</p>
                    </div>
                    <div className="header-actions">
                        <button
                            className="theme-toggle"
                            onClick={toggleTheme}
                            title={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
                        >
                            {theme === 'light' ? '🌙' : '☀️'}
                        </button>
                        <div className={`status-badge ${backendStatus}`}>
                            <span className="status-dot"></span>
                            Backend {backendStatus === 'online' ? 'Online' : backendStatus === 'offline' ? 'Offline' : 'Checking...'}
                        </div>
                    </div>
                </header>

                <div className="main-card">
                    <form onSubmit={handleSubmit}>
                        <div className="form-group">
                            <label htmlFor="scenario">Select Scenario</label>
                            <select
                                id="scenario"
                                value={scenario}
                                onChange={(e) => setScenario(e.target.value)}
                                className="select-input"
                            >
                                {Object.keys(DEMO_DATA).map((key) => (
                                    <option key={key} value={key}>{key}</option>
                                ))}
                            </select>
                        </div>

                        <div className="form-group">
                            <label htmlFor="title">Task Title</label>
                            <input
                                id="title"
                                type="text"
                                value={taskTitle}
                                onChange={(e) => setTaskTitle(e.target.value)}
                                disabled={isDisabled}
                                className="text-input"
                                placeholder="Enter task title..."
                            />
                        </div>

                        <div className="form-group">
                            <label htmlFor="description">Task Description</label>
                            <textarea
                                id="description"
                                value={taskDesc}
                                onChange={(e) => setTaskDesc(e.target.value)}
                                disabled={isDisabled}
                                className="textarea-input"
                                rows="8"
                                placeholder="Enter detailed task description..."
                            />
                        </div>

                        <div className="form-group">
                            <label htmlFor="github">GitHub Repository URL (Optional)</label>
                            <input
                                id="github"
                                type="text"
                                value={githubUrl}
                                onChange={(e) => setGithubUrl(e.target.value)}
                                disabled={isDisabled}
                                className="text-input"
                                placeholder="https://github.com/user/repo"
                            />
                        </div>

                        <div className="form-group">
                            <label htmlFor="pdf">Project Documentation (PDF - Optional)</label>
                            <input
                                id="pdf"
                                type="file"
                                accept=".pdf"
                                onChange={handleFileChange}
                                disabled={isDisabled}
                                className="file-input"
                            />
                        </div>

                        <div className="form-group">
                            <label htmlFor="name">Your Name</label>
                            <input
                                id="name"
                                type="text"
                                value={submittedBy}
                                onChange={(e) => setSubmittedBy(e.target.value)}
                                className="text-input"
                                placeholder="Enter your name..."
                            />
                        </div>

                        <button type="submit" className="submit-btn" disabled={loading}>
                            {loading ? (
                                <>
                                    <span className="spinner"></span>
                                    Analyzing...
                                </>
                            ) : (
                                'Analyze Submission'
                            )}
                        </button>
                    </form>

                    {error && (
                        <div className="error-box">
                            <strong>Error:</strong> {error}
                        </div>
                    )}

                    {result && (
                        <div className="results-section">
                            <div className="divider"></div>

                            <div className="status-header" style={{ color: getStatusColor(result.review.status) }}>
                                <h2>Status: {result.review.status.toUpperCase()}</h2>
                            </div>

                            <div className="metrics-grid">
                                <div className="metric-card">
                                    <div className="metric-label">Score</div>
                                    <div className="metric-value">{result.review.score}/100</div>
                                </div>
                                <div className="metric-card">
                                    <div className="metric-label">Readiness</div>
                                    <div className="metric-value">{result.review.readiness_percent}%</div>
                                </div>
                                <div className="metric-card">
                                    <div className="metric-label">Eval Time</div>
                                    <div className="metric-value">{result.review.meta.evaluation_time_ms}ms</div>
                                </div>
                            </div>

                            <div className="analysis-section">
                                <h3>Technical Analysis</h3>
                                <div className="progress-grid">
                                    <div className="progress-item">
                                        <div className="progress-header">
                                            <span>Technical Quality (Repo)</span>
                                            <span>{result.review.analysis.technical_quality}%</span>
                                        </div>
                                        <div className="progress-bar">
                                            <div className="progress-fill" style={{ width: `${result.review.analysis.technical_quality}%` }}></div>
                                        </div>
                                    </div>
                                    <div className="progress-item">
                                        <div className="progress-header">
                                            <span>Clarity (Desc)</span>
                                            <span>{result.review.analysis.clarity}%</span>
                                        </div>
                                        <div className="progress-bar">
                                            <div className="progress-fill" style={{ width: `${result.review.analysis.clarity}%` }}></div>
                                        </div>
                                    </div>
                                    <div className="progress-item">
                                        <div className="progress-header">
                                            <span>Discipline Signals (PDF)</span>
                                            <span>{result.review.analysis.discipline_signals}%</span>
                                        </div>
                                        <div className="progress-bar">
                                            <div className="progress-fill" style={{ width: `${result.review.analysis.discipline_signals}%` }}></div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            {result.review.failure_reasons && result.review.failure_reasons.length > 0 && (
                                <div className="info-section failure">
                                    <h3>❌ Failure Reasons & Gaps</h3>
                                    <ul>
                                        {result.review.failure_reasons.map((reason, idx) => (
                                            <li key={idx}>{reason}</li>
                                        ))}
                                    </ul>
                                </div>
                            )}

                            {result.review.improvement_hints && result.review.improvement_hints.length > 0 && (
                                <div className="info-section hints">
                                    <h3>✨ Optimization Hints</h3>
                                    <ul>
                                        {result.review.improvement_hints.map((hint, idx) => (
                                            <li key={idx}>{hint}</li>
                                        ))}
                                    </ul>
                                </div>
                            )}

                            <div className="next-task-section">
                                <div className="next-task-card">
                                    <h3>💡 Recommended Next Step</h3>
                                    <p className="next-task-title">{result.nextTask.title}</p>
                                    <p className="next-task-rationale"><strong>Objective:</strong> {result.nextTask.objective}</p>
                                    <p className="next-task-rationale"><strong>Focus:</strong> {result.nextTask.focus_area}</p>
                                </div>
                            </div>

                            <div className="toast">
                                ✅ Evaluation complete in {result.review.meta.evaluation_time_ms}ms using {result.review.meta.mode} mode.
                            </div>
                        </div>
                    )}
                </div>

                <footer className="footer">
                    <p>Production Locked • Deterministic Engine v2.0</p>
                </footer>
            </div>
        </div>
    );
}

export default App;
