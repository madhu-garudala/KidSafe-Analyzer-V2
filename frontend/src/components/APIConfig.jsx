import React from 'react';

const APIConfig = ({ isInitialized }) => {
  return (
    <div className="status-badge-container">
      <div className={`status-badge ${isInitialized ? 'status-ready' : 'status-loading'}`}>
        <div className="status-icon">
          {isInitialized ? (
            '✅'
          ) : (
            <div className="spinner small"></div>
          )}
        </div>
        <div className="status-text">
          <div className="status-title">
            {isInitialized ? 'System Ready' : 'Initializing...'}
          </div>
          {!isInitialized && (
            <div className="status-subtitle">Please wait</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default APIConfig;

