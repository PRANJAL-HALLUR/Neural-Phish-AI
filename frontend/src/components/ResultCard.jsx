import { motion } from 'framer-motion';
import { Info, Globe, Key } from 'lucide-react';
import './ResultCard.css';

const ResultCard = ({ result }) => {
  if (!result) return null;

  const { prediction, confidence, risk_level, reason, domain_status, keywords_detected } = result;
  
  let theme = 'safe';
  let iconEmoji = '✅';
  let title = 'Safe';
  let glowColor = 'rgba(34, 197, 94, 0.4)';

  if (prediction === 'Phishing' || risk_level === 'High') {
    theme = 'danger';
    iconEmoji = '🚨';
    title = 'Phishing';
    glowColor = 'rgba(239, 68, 68, 0.4)';
  } else if (prediction === 'Suspicious' || risk_level === 'Medium') {
    theme = 'warning';
    iconEmoji = '⚠️';
    title = 'Suspicious';
    glowColor = 'rgba(250, 204, 21, 0.4)';
  }

  return (
    <motion.div 
      className={`result-card glass-panel theme-${theme}`}
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      whileHover={{ scale: 1.02, boxShadow: `0 0 30px ${glowColor}` }}
      transition={{ duration: 0.4 }}
    >
      <div className="result-header">
        <span style={{ fontSize: '2rem', marginRight: '0.5rem' }}>{iconEmoji}</span>
        <h2 className="result-title">
          {title} Detected
        </h2>
      </div>

      <div className="confidence-section">
        <div className="confidence-header">
          <span>Threat Confidence</span>
          <span className="confidence-value">{confidence}%</span>
        </div>
        <div className="progress-bar-bg">
          <motion.div 
            className="progress-bar-fill"
            initial={{ width: 0 }}
            animate={{ width: `${confidence}%` }}
            transition={{ duration: 1, delay: 0.2, ease: "easeOut" }}
          />
        </div>
      </div>

      <div className="details-grid">
        <div className="detail-item">
          <span className="detail-label">Risk Level</span>
          <span className="detail-value">{risk_level}</span>
        </div>
        <div className="detail-item">
          <span className="detail-label">Explanation</span>
          <span className="detail-value reason-text">
            <Info size={16} />
            {reason}
          </span>
        </div>
        
        {domain_status && (
          <div className="detail-item">
            <span className="detail-label">Domain Name</span>
            <span className="detail-value reason-text" style={{ color: 'var(--text-main)' }}>
              <Globe size={16} style={{ color: 'var(--accent)' }}/>
              {domain_status}
            </span>
          </div>
        )}

        {keywords_detected && keywords_detected.length > 0 && (
          <div className="detail-item">
            <span className="detail-label">Detected Keywords</span>
            <span className="detail-value reason-text" style={{ color: 'var(--text-main)', display: 'flex', flexWrap: 'wrap', gap: '4px' }}>
              <Key size={16} style={{ color: 'var(--accent)' }}/>
              {keywords_detected.map((kw, i) => (
                <span key={i} style={{ background: 'rgba(255,255,255,0.1)', padding: '2px 6px', borderRadius: '4px', fontSize: '0.85rem' }}>{kw}</span>
              ))}
            </span>
          </div>
        )}
      </div>

      <div className="disclaimer" style={{ marginTop: '1.5rem', fontSize: '0.85rem', color: 'var(--text-muted)', textAlign: 'center', fontStyle: 'italic', opacity: 0.8 }}>
        * This system prioritizes safety and may flag some safe links.
      </div>
    </motion.div>
  );
};

export default ResultCard;
