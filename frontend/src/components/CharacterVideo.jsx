import React, { useState, useEffect } from 'react';

const CharacterVideo = ({ videoData, productName }) => {
  const [videoLoaded, setVideoLoaded] = useState(false);

  if (!videoData) {
    return null;
  }

  const { success, video_url, script, has_api } = videoData;

  // If D-ID API not configured
  if (!has_api) {
    return (
      <div className="character-section">
        <div className="character-card no-video">
          <div className="character-header">
            <div className="character-avatar">🐶</div>
            <div>
              <h3>Berry's Quick Take: {productName}</h3>
              <p>Video generation requires D-ID API setup</p>
            </div>
          </div>
          {script && (
            <div className="character-message">
              <p>{script}</p>
            </div>
          )}
          <div className="setup-instructions">
            <h4>🎬 Enable Animated Videos:</h4>
            <ol>
              <li>Sign up at <a href="https://studio.d-id.com" target="_blank" rel="noopener noreferrer">D-ID Studio</a> (free trial: 20 credits)</li>
              <li>Get your API key from Account Settings</li>
              <li>Add to <code>backend/.env</code>: <code>DID_API_KEY=your_key_here</code></li>
              <li>Restart backend</li>
            </ol>
          </div>
        </div>
      </div>
    );
  }

  // Video is being generated
  if (!success && !video_url) {
    return (
      <div className="character-section">
        <div className="character-card">
          <div className="character-header">
            <div className="character-avatar">🐶</div>
            <div>
              <h3>Berry is preparing a video for you...</h3>
              <p>Creating animated explanation</p>
            </div>
          </div>
          <div className="video-generating">
            <div className="spinner"></div>
            <p className="generating-text">Generating animated video...</p>
            <p className="generating-subtext">This takes about 15-30 seconds</p>
            {script && (
              <div className="preview-message">
                <strong>Preview:</strong> {script}
              </div>
            )}
          </div>
        </div>
      </div>
    );
  }

  // Video ready!
  if (success && video_url) {
    return (
      <div className="character-section">
        <div className="character-card">
          <div className="character-header">
            <div className="character-avatar">🐶</div>
            <div>
              <h3>🎬 Berry Explains: {productName}</h3>
              <p>Watch the animated explanation!</p>
            </div>
          </div>
          <div className="video-wrapper">
            {!videoLoaded && (
              <div className="video-loading-overlay">
                <div className="spinner"></div>
                <p>Loading video...</p>
              </div>
            )}
            <video
              className="character-video"
              controls
              autoPlay
              onLoadedData={() => setVideoLoaded(true)}
              style={{ display: videoLoaded ? 'block' : 'none' }}
            >
              <source src={video_url} type="video/mp4" />
              Your browser does not support the video tag.
            </video>
          </div>
        </div>
      </div>
    );
  }

  // Video generation failed
  return (
    <div className="character-section">
      <div className="character-card error">
        <div className="character-header">
          <div className="character-avatar">🐶</div>
          <div>
            <h3>Berry's Message: {productName}</h3>
            <p>Video couldn't be generated</p>
          </div>
        </div>
        {script && (
          <div className="character-message">
            <p>{script}</p>
          </div>
        )}
        <div className="error-info">
          <p>⚠️ Video generation failed. Check backend logs for details.</p>
        </div>
      </div>
    </div>
  );
};

export default CharacterVideo;

