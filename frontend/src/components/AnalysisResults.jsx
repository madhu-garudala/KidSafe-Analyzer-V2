import React from 'react';

const AnalysisResults = ({ result }) => {
  // Convert markdown-style formatting to HTML
  const formatAnalysis = (text) => {
    let html = text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\n### (.*?)\n/g, '<h3>$1</h3>')
      .replace(/\n## (.*?)\n/g, '<h3>$1</h3>')
      .replace(/\n# (.*?)\n/g, '<h3>$1</h3>')
      .replace(/\n\n/g, '</p><p>')
      .replace(/\n- /g, '</li><li>')
      .replace(/<li>/i, '<ul><li>')
      .replace(/(<li>.*)/i, '$1</ul>');

    // Wrap in paragraph tags if not already wrapped
    if (!html.startsWith('<')) {
      html = '<p>' + html + '</p>';
    }

    return html;
  };

  return (
    <div className="card" id="results-card">
      <div className="card-header">
        <h2>📊 Analysis Results</h2>
        <p>{result.cereal_name}</p>
      </div>

      <div className="card-body">
        <div
          className="analysis-results"
          dangerouslySetInnerHTML={{ __html: formatAnalysis(result.analysis) }}
        />
      </div>
    </div>
  );
};

export default AnalysisResults;

