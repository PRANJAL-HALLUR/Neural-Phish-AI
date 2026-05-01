import { motion } from 'framer-motion';
import './RiskMeter.css';

const RiskMeter = ({ confidence, isSafe }) => {
  const radius = 45;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (confidence / 100) * circumference;

  const isHighRisk = confidence > 80;
  const themeClass = isSafe ? 'safe' : (isHighRisk ? 'danger' : 'warning');
  
  // Choose stroke color based on theme
  const getStrokeColor = () => {
    if (isSafe) return 'var(--success)';
    if (isHighRisk) return 'var(--danger)';
    return 'var(--warning)';
  };

  return (
    <div className="risk-meter-container">
      <div className={`risk-meter-wrapper meter-${themeClass}`}>
        <svg className="risk-meter-svg" width="120" height="120" viewBox="0 0 100 100">
          {/* Background circle */}
          <circle
            cx="50"
            cy="50"
            r={radius}
            fill="transparent"
            stroke="rgba(255, 255, 255, 0.1)"
            strokeWidth="8"
          />
          {/* Progress circle */}
          <motion.circle
            cx="50"
            cy="50"
            r={radius}
            fill="transparent"
            stroke={getStrokeColor()}
            strokeWidth="8"
            strokeDasharray={circumference}
            initial={{ strokeDashoffset: circumference }}
            animate={{ strokeDashoffset }}
            transition={{ duration: 1.5, ease: "easeOut", delay: 0.2 }}
            strokeLinecap="round"
            style={{
              transformOrigin: '50% 50%',
              transform: 'rotate(-90deg)',
              filter: `drop-shadow(0 0 4px ${getStrokeColor()})`
            }}
          />
        </svg>
        <div className="risk-meter-text">
          <motion.span 
            className="risk-meter-value"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.8 }}
          >
            {confidence}%
          </motion.span>
        </div>
      </div>
    </div>
  );
};

export default RiskMeter;
