import { useState } from 'react';
import Header from './components/Header';
import DetectionPanel from './components/DetectionPanel';
import HistoryPanel from './components/HistoryPanel';
import './App.css';

function App() {
  const [history, setHistory] = useState([]);

  const addHistoryItem = (item) => {
    setHistory((prev) => {
      if (prev.length > 0 && prev[0].input === item.input) {
        return prev;
      }
      const newHistory = [item, ...prev];
      if (newHistory.length > 5) return newHistory.slice(0, 5);
      return newHistory;
    });
  };

  return (
    <div className="app-container">
      <Header />
      
      <main className="main-content">
        <div className="left-column">
          <DetectionPanel onResult={addHistoryItem} />
        </div>
        
        <div className="right-column">
          <HistoryPanel history={history} />
        </div>
      </main>
    </div>
  );
}

export default App;
