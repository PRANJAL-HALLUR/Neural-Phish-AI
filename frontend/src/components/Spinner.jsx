import { motion } from 'framer-motion';
import './Spinner.css';

const Spinner = () => {
  return (
    <div className="spinner-container">
      <motion.div
        className="spinner"
        animate={{ rotate: 360 }}
        transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
      />
      <span className="spinner-text">Analyzing...</span>
    </div>
  );
};

export default Spinner;
