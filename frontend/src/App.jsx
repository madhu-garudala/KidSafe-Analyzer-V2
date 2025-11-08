import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import APIConfig from './components/APIConfig';
import CerealSelector from './components/CerealSelector';
import AnalysisResults from './components/AnalysisResults';
import Chatbot from './components/Chatbot';
import { checkSystemStatus } from './services/api';
import './App.css';

function App() {
  const [isInitialized, setIsInitialized] = useState(false);
  const [selectedCereal, setSelectedCereal] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);

  useEffect(() => {
    // Check system status on mount and periodically if not initialized
    const checkStatus = () => {
      checkSystemStatus()
        .then(data => {
          if (data.initialized) {
            setIsInitialized(true);
          }
        })
        .catch(err => console.log('Could not check system status:', err));
    };

    // Initial check
    checkStatus();

    // Poll every 3 seconds if not initialized
    const interval = setInterval(() => {
      if (!isInitialized) {
        checkStatus();
      }
    }, 3000);

    // Cleanup interval on unmount or when initialized
    return () => clearInterval(interval);
  }, [isInitialized]);

  const handleCerealSelect = (cereal) => {
    setSelectedCereal(cereal);
    setAnalysisResult(null); // Clear previous results
  };

  const handleAnalysisComplete = (result) => {
    setAnalysisResult(result);
  };

  return (
    <div className="app">
      <div className="container">
        <div className="header-with-status">
          <Header />
          <APIConfig 
            isInitialized={isInitialized}
          />
        </div>
        
        <main className="main-content">
          <CerealSelector 
            isEnabled={isInitialized}
            onCerealSelect={handleCerealSelect}
            selectedCereal={selectedCereal}
            onAnalysisComplete={handleAnalysisComplete}
          />
          
          {analysisResult && (
            <>
              <AnalysisResults result={analysisResult} />
              <Chatbot 
                cerealName={analysisResult.cereal_name}
                ingredients={analysisResult.ingredients}
                analysisResult={analysisResult.analysis}
              />
            </>
          )}
        </main>

        <footer className="footer">
          <p>AI-powered food safety analysis for concerned parents</p>
        </footer>
      </div>
    </div>
  );
}

export default App;

