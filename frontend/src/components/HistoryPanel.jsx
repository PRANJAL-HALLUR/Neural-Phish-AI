import { Clock } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import './HistoryPanel.css';

const HistoryPanel = ({ history }) => {
  return (
    <div className="history-panel glass-panel">
      <div className="history-header">
        <Clock size={20} className="accent-text" />
        <h2>Recent Scans</h2>
      </div>

      <div className="history-list">
        {history.length === 0 ? (
          <div className="empty-history">
            No scans yet. Your recent activity will appear here.
          </div>
        ) : (
          <AnimatePresence>
            {history.map((item) => {
              let statusText = 'Safe';
              let emoji = '✅';
              let borderColor = 'border-safe';
              let textColor = 'text-safe';

              if (item.prediction === 'Phishing' || item.risk_level === 'High') {
                statusText = 'Phishing';
                emoji = '🚨';
                borderColor = 'border-danger';
                textColor = 'text-danger';
              } else if (item.prediction === 'Suspicious' || item.risk_level === 'Medium') {
                statusText = 'Suspicious';
                emoji = '⚠️';
                borderColor = 'border-warning';
                textColor = 'text-warning';
              }
              
              return (
                <motion.div 
                  key={item.id}
                  className={`history-item ${borderColor}`}
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, scale: 0.9 }}
                  transition={{ duration: 0.3 }}
                >
                  <div className="history-item-header">
                    <span className="history-type">{item.type.toUpperCase()}</span>
                    <span className="history-time">{item.timestamp}</span>
                  </div>
                  
                  <div className="history-content">
                    <div className="history-input-preview">
                      {item.input.length > 30 ? item.input.substring(0, 30) + '...' : item.input}
                    </div>
                    <div className={`history-status ${textColor}`}>
                      <span style={{ fontSize: '1rem', marginRight: '4px' }}>{emoji}</span>
                      {statusText}
                    </div>
                  </div>
                </motion.div>
              );
            })}
          </AnimatePresence>
        )}
      </div>
    </div>
  );
};

export default HistoryPanel;
