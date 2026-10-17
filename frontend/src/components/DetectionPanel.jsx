import { useState, useCallback, useEffect } from 'react';
import { MessageSquare, Link, Scan } from 'lucide-react';
import { motion } from 'framer-motion';
import ResultCard from './ResultCard';
import Spinner from './Spinner';
import './DetectionPanel.css';

// Base API resolution:
// In production single-service or Vite dev (with proxy), defaults to relative '/predict'
// If an external URL is explicitly supplied in VITE_API_BASE_URL, normalize and use it.
const RAW_API_BASE = (import.meta.env.VITE_API_BASE_URL || '').trim().replace(/\/+$/, '');
const API_PREDICT_BASE = RAW_API_BASE.endsWith('/predict')
  ? RAW_API_BASE
  : RAW_API_BASE
    ? `${RAW_API_BASE}/predict`
    : '/predict';

const DetectionPanel = ({ onResult }) => {
  const [activeTab, setActiveTab] = useState('message');
  const [inputValue, setInputValue] = useState(''); // Immediate input state
  const [input, setInput] = useState(''); // Debounced input state
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  // 300ms Input Debounce
  useEffect(() => {
    const timer = setTimeout(() => {
      setInput(inputValue);
    }, 300);
    return () => clearTimeout(timer);
  }, [inputValue]);

  const handleScan = useCallback(async () => {
    const currentInput = inputValue.trim();
    if (!currentInput) {
      setError('Please enter some input to analyze.');
      return;
    }

    if (activeTab === 'url') {
      const urlPattern = /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/i;
      if (!urlPattern.test(currentInput)) {
        setError('Please enter a valid URL.');
        return;
      }
    }

    setError('');
    setLoading(true);
    setResult(null);

    try {
      const endpoint = activeTab === 'url' ? `${API_PREDICT_BASE}/url` : `${API_PREDICT_BASE}/message`;
      const payload = activeTab === 'url' ? { url: currentInput } : { text: currentInput };

      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        throw new Error(`Server responded with status: ${response.status}`);
      }

      const data = await response.json();

      setResult(data);
      onResult({
        id: Date.now(),
        type: activeTab,
        input: currentInput,
        ...data,
        timestamp: new Date().toLocaleTimeString()
      });

    } catch (err) {
      console.error(err);
      setError('Failed to connect to the analysis engine. Please try again.');
    } finally {
      setLoading(false);
    }
  }, [activeTab, inputValue, onResult]);

  return (
    <div className="detection-panel">
      <div className="tabs">
        <button
          className={`tab-btn ${activeTab === 'message' ? 'active' : ''}`}
          onClick={() => { setActiveTab('message'); setResult(null); setError(''); }}
        >
          <MessageSquare size={18} />
          Message Detection
        </button>
        <button
          className={`tab-btn ${activeTab === 'url' ? 'active' : ''}`}
          onClick={() => { setActiveTab('url'); setResult(null); setError(''); }}
        >
          <Link size={18} />
          URL Detection
        </button>
      </div>

      <div className="input-container glass-panel">
        <div className="input-wrapper">
          {activeTab === 'url' ? (
            <input
              type="text"
              placeholder="Enter URL to analyze (e.g., http://suspicious-link.com)"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              className="cyber-input"
            />
          ) : (
            <textarea
              placeholder="Paste message text here..."
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              className="cyber-input textarea"
              rows={4}
            />
          )}
        </div>

        {error && <div className="error-message">{error}</div>}

        <motion.button
          className="scan-btn"
          whileHover={{ scale: 1.02, boxShadow: "0 0 20px rgba(56, 189, 248, 0.4)" }}
          whileTap={{ scale: 0.98 }}
          onClick={handleScan}
          disabled={loading}
        >
          <Scan size={20} />
          {loading ? 'Scanning...' : 'Analyze Now'}
        </motion.button>
      </div>

      {loading && <Spinner />}

      {!loading && result && <ResultCard result={result} />}
    </div>
  );
};

export default DetectionPanel;
