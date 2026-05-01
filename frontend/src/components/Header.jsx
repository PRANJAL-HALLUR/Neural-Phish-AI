import { ShieldAlert } from 'lucide-react';
import { motion } from 'framer-motion';
import './Header.css';

const Header = () => {
  return (
    <motion.header 
      className="header glass-panel"
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="logo-container">
        <ShieldAlert className="logo-icon" size={32} />
        <h1 className="logo-text">Neural<span className="accent-text">Phish</span></h1>
      </div>
      <div className="status-badge">
        <span className="status-dot"></span>
        System Online
      </div>
    </motion.header>
  );
};

export default Header;
