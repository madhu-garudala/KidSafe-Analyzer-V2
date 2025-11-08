import React, { useState, useRef, useEffect } from 'react';
import { sendChatMessage } from '../services/api';

const Chatbot = ({ cerealName, ingredients, analysisResult }) => {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: `Hi! I'm here to answer any questions you have about the ingredients in ${cerealName}. Feel free to ask me anything!`,
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = input.trim();
    setInput('');

    // Add user message to chat
    setMessages((prev) => [...prev, { role: 'user', content: userMessage }]);
    setLoading(true);

    try {
      const response = await sendChatMessage({
        cereal_name: cerealName,
        ingredients: ingredients,
        previous_analysis: analysisResult,
        question: userMessage,
        chat_history: messages,
      });

      if (response.success) {
        setMessages((prev) => [
          ...prev,
          { role: 'assistant', content: response.answer },
        ]);
      } else {
        setMessages((prev) => [
          ...prev,
          {
            role: 'assistant',
            content: `Sorry, I encountered an error: ${response.error}`,
          },
        ]);
      }
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: `Network error: ${error.message}`,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="card chatbot-card">
      <div className="card-header">
        <h2>💬 Ask Questions About Ingredients</h2>
        <p>Chat with our AI assistant about {cerealName}</p>
      </div>

      <div className="card-body">
        <div className="chat-container">
          <div className="chat-messages">
            {messages.map((message, index) => (
              <div
                key={index}
                className={`chat-message ${
                  message.role === 'user' ? 'user-message' : 'assistant-message'
                }`}
              >
                <div className="message-avatar">
                  {message.role === 'user' ? '👤' : '🤖'}
                </div>
                <div className="message-content">
                  <div className="message-text">{message.content}</div>
                </div>
              </div>
            ))}
            {loading && (
              <div className="chat-message assistant-message">
                <div className="message-avatar">🤖</div>
                <div className="message-content">
                  <div className="message-text typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <form onSubmit={handleSubmit} className="chat-input-form">
            <div className="chat-input-wrapper">
              <input
                type="text"
                className="chat-input"
                placeholder="Ask a question about the ingredients..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                disabled={loading}
              />
              <button
                type="submit"
                className="chat-send-btn"
                disabled={loading || !input.trim()}
              >
                {loading ? '⏳' : '📤'}
              </button>
            </div>
          </form>

          <div className="chat-suggestions">
            <p className="suggestions-title">Suggested questions:</p>
            <div className="suggestion-chips">
              <button
                className="suggestion-chip"
                onClick={() =>
                  setInput('What are the health concerns with this cereal?')
                }
                disabled={loading}
              >
                Health concerns?
              </button>
              <button
                className="suggestion-chip"
                onClick={() =>
                  setInput('Are there any artificial ingredients?')
                }
                disabled={loading}
              >
                Artificial ingredients?
              </button>
              <button
                className="suggestion-chip"
                onClick={() =>
                  setInput('Is this suitable for children under 5?')
                }
                disabled={loading}
              >
                Safe for young kids?
              </button>
              <button
                className="suggestion-chip"
                onClick={() => setInput('What does "natural flavors" mean?')}
                disabled={loading}
              >
                Natural flavors?
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Chatbot;

