import React, { useState, useEffect } from 'react';
import { getCereals } from '../services/api';

const CerealSelector = ({ isEnabled, onCerealSelect, selectedCereal, onAnalysisComplete }) => {
  const [cereals, setCereals] = useState([]);
  const [precomputedAnalyses, setPrecomputedAnalyses] = useState({});
  const [loading, setLoading] = useState(true);
  const [notification, setNotification] = useState(null);
  const [customMode, setCustomMode] = useState(false);
  const [customProductName, setCustomProductName] = useState('');
  const [customIngredients, setCustomIngredients] = useState('');
  const [analyzing, setAnalyzing] = useState(false);

  useEffect(() => {
    // Load cereals and pre-computed analyses on mount
    loadCereals();
    loadPrecomputedAnalyses();
  }, []);

  const loadCereals = async () => {
    try {
      const data = await getCereals();
      setCereals(data);
    } catch (error) {
      console.error('Failed to load cereals:', error);
      showNotification('Failed to load cereals', 'error');
    }
  };

  const loadPrecomputedAnalyses = async () => {
    try {
      const response = await fetch('/precomputed-analyses.json');
      if (response.ok) {
        const data = await response.json();
        setPrecomputedAnalyses(data);
        console.log('✅ Loaded pre-computed analyses - results will display instantly!');
        showNotification('Ready! Select a cereal for instant analysis', 'info');
      } else {
        console.warn('⚠️  Pre-computed analyses not found.');
        showNotification('Pre-computed data missing. Please regenerate.', 'error');
      }
    } catch (err) {
      console.error('Error loading pre-computed analyses:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectChange = (e) => {
    const selectedBrand = e.target.value;
    setCustomMode(false);
    setCustomProductName('');
    setCustomIngredients('');
    
    if (selectedBrand) {
      const cereal = cereals.find((c) => c.brand === selectedBrand);
      onCerealSelect(cereal);
      
      // Instantly display pre-computed result
      if (precomputedAnalyses[selectedBrand]) {
        console.log('⚡ Displaying pre-computed analysis (instant!)');
        onAnalysisComplete(precomputedAnalyses[selectedBrand]);
        
        // Scroll to results after a brief delay
        setTimeout(() => {
          const resultsCard = document.getElementById('results-card');
          if (resultsCard) {
            resultsCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
          }
        }, 100);
      } else {
        showNotification('Analysis not found for this cereal', 'error');
      }
    } else {
      onCerealSelect(null);
    }
  };

  const handleCustomSearch = async () => {
    if (!customProductName.trim()) {
      showNotification('Please enter a product name', 'error');
      return;
    }
    
    // First, check if it matches a pre-computed cereal
    const matchedCereal = cereals.find(c => 
      c.brand.toLowerCase().includes(customProductName.toLowerCase())
    );
    
    if (matchedCereal && precomputedAnalyses[matchedCereal.brand]) {
      console.log('⚡ Found in pre-computed database!');
      onCerealSelect(matchedCereal);
      onAnalysisComplete(precomputedAnalyses[matchedCereal.brand]);
      showNotification('Found in database!', 'success');
      
      setTimeout(() => {
        const resultsCard = document.getElementById('results-card');
        if (resultsCard) {
          resultsCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      }, 100);
      return;
    }
    
    // Not in local database - search online
    console.log('🔍 Searching online for product ingredients...');
    setAnalyzing(true);
    showNotification('Searching online for product information...', 'info');
    
    try {
      const { searchProduct } = await import('../services/api');
      const searchResult = await searchProduct(customProductName);
      
      if (searchResult.found && searchResult.ingredients) {
        // Found ingredients online! Auto-analyze them
        console.log('✅ Found ingredients online! Auto-analyzing...');
        showNotification('Found ingredients! Analyzing...', 'success');
        
        // Automatically analyze the found ingredients
        const { analyzeIngredients } = await import('../services/api');
        const analysisResult = await analyzeIngredients(
          customProductName,
          searchResult.ingredients
        );
        
        if (analysisResult.success) {
          onCerealSelect({ 
            brand: customProductName, 
            ingredients: searchResult.ingredients 
          });
          onAnalysisComplete(analysisResult);
          showNotification('Analysis complete!', 'success');
          
          setTimeout(() => {
            const resultsCard = document.getElementById('results-card');
            if (resultsCard) {
              resultsCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
          }, 100);
        } else {
          showNotification('Analysis failed', 'error');
        }
      } else {
        // Not found online - ask user to enter manually
        console.log('❌ Product not found online');
        setCustomMode(true);
        setCustomIngredients(''); // Clear any previous ingredients
        showNotification(searchResult.message || 'Product not found. Please enter ingredients manually.', 'info');
      }
    } catch (error) {
      console.error('Search error:', error);
      setCustomMode(true);
      showNotification('Could not search online. Please enter ingredients manually.', 'error');
    } finally {
      setAnalyzing(false);
    }
  };

  const handleCustomAnalyze = async () => {
    if (!customProductName.trim() || !customIngredients.trim()) {
      showNotification('Please enter both product name and ingredients', 'error');
      return;
    }

    setAnalyzing(true);
    
    try {
      const { analyzeIngredients } = await import('../services/api');
      const result = await analyzeIngredients(customProductName, customIngredients);

      if (result.success) {
        onCerealSelect({ brand: customProductName, ingredients: customIngredients });
        onAnalysisComplete(result);
        showNotification('Analysis complete!', 'success');
        
        setTimeout(() => {
          const resultsCard = document.getElementById('results-card');
          if (resultsCard) {
            resultsCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
          }
        }, 100);
      } else {
        showNotification(`Error: ${result.error}`, 'error');
      }
    } catch (error) {
      showNotification(`Failed to analyze: ${error.message}`, 'error');
    } finally {
      setAnalyzing(false);
    }
  };

  const showNotification = (message, type) => {
    setNotification({ message, type });
    setTimeout(() => setNotification(null), 3000);
  };

  return (
    <>
      <div className="card">
        <div className="card-header">
          <h2>📦 Select a Product</h2>
          <p>Choose from database or search for any product</p>
        </div>

        <div className="card-body">
          {loading ? (
            <div className="loading">
              <div className="spinner"></div>
              <p>Loading database...</p>
            </div>
          ) : (
            <>
              <div className="dual-input-wrapper">
                <div className="input-group">
                  <label htmlFor="cereal-select" className="select-label">
                    <span className="label-icon">📋</span>
                    Quick Select (Pre-computed)
                  </label>
                  <select
                    id="cereal-select"
                    className="cereal-select"
                    onChange={handleSelectChange}
                    value={selectedCereal?.brand || ''}
                    disabled={Object.keys(precomputedAnalyses).length === 0}
                  >
                    <option value="">-- Choose from database --</option>
                    {cereals.map((cereal, index) => (
                      <option key={index} value={cereal.brand}>
                        {cereal.brand}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="input-group">
                  <label htmlFor="custom-search" className="select-label">
                    <span className="label-icon">🔍</span>
                    Search Any Product
                  </label>
                  <div className="search-wrapper">
                    <input
                      id="custom-search"
                      type="text"
                      className="custom-search-input"
                      placeholder="Enter product name..."
                      value={customProductName}
                      onChange={(e) => setCustomProductName(e.target.value)}
                      onKeyPress={(e) => e.key === 'Enter' && handleCustomSearch()}
                    />
                    <button 
                      className="search-btn"
                      onClick={handleCustomSearch}
                      disabled={!customProductName.trim()}
                    >
                      Search
                    </button>
                  </div>
                </div>
              </div>

              {customMode && (
                <div className="custom-input-section">
                  <div className="info-message">
                    <span className="info-icon">ℹ️</span>
                    <span>Product not found online. Please enter the ingredients list manually:</span>
                  </div>
                  <div style={{ 
                    fontSize: '0.85rem', 
                    color: '#92400e', 
                    marginBottom: '1rem',
                    fontStyle: 'italic'
                  }}>
                    Tip: Find the ingredients on the product packaging or manufacturer's website
                  </div>
                  <textarea
                    className="ingredients-input"
                    placeholder="Paste or type the ingredients list here..."
                    value={customIngredients}
                    onChange={(e) => setCustomIngredients(e.target.value)}
                    rows="4"
                  />
                  <button
                    className="analyze-btn"
                    onClick={handleCustomAnalyze}
                    disabled={analyzing || !customIngredients.trim()}
                  >
                    {analyzing ? (
                      <>
                        <span className="spinner small"></span> Analyzing...
                      </>
                    ) : (
                      <>
                        Analyze Ingredients <span className="btn-icon">→</span>
                      </>
                    )}
                  </button>
                </div>
              )}

              {selectedCereal && !customMode && (
                <div className="selected-info">
                  <div className="info-badge">
                    <span className="badge-icon">✓</span>
                    <span>{selectedCereal.brand}</span>
                  </div>
                </div>
              )}

              {analyzing && (
                <div className="loading">
                  <div className="spinner"></div>
                  <p>Analyzing ingredients... This may take up to 10 seconds</p>
                </div>
              )}
            </>
          )}
        </div>
      </div>

      {notification && (
        <div className={`notification notification-${notification.type}`}>
          {notification.message}
        </div>
      )}
    </>
  );
};

export default CerealSelector;

