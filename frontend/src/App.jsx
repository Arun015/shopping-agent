import React, { useState, useRef, useEffect } from 'react';
import ChatMessage from './components/ChatMessage';
import ChatInput from './components/ChatInput';
import SuggestedQueries from './components/SuggestedQueries';
import { sendMessage } from './services/api';

function App() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (message) => {
    setMessages((prev) => [...prev, { text: message, isUser: true }]);
    setLoading(true);

    try {
      const response = await sendMessage(message, sessionId);
      setSessionId(response.session_id);
      setMessages((prev) => [
        ...prev,
        { text: response.response, isUser: false },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          text: 'Sorry, something went wrong. Please try again.',
          isUser: false,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-6xl mx-auto px-4 py-4">
          <h1 className="text-2xl font-bold text-gray-900">
            Mobile Shopping Agent
          </h1>
          <p className="text-sm text-gray-600">
            Find the perfect phone for your needs
          </p>
        </div>
      </header>

      <main className="flex-1 overflow-hidden flex flex-col max-w-6xl w-full mx-auto">
        <div className="flex-1 overflow-y-auto px-4 py-6">
          {messages.length === 0 ? (
            <div className="max-w-3xl mx-auto">
              <div className="text-center mb-8">
                <h2 className="text-3xl font-bold text-gray-900 mb-2">
                  Welcome! 👋
                </h2>
                <p className="text-gray-600">
                  I'm your AI shopping assistant. Ask me anything about mobile phones!
                </p>
              </div>
              <SuggestedQueries onQueryClick={handleSendMessage} />
            </div>
          ) : (
            <div className="max-w-4xl mx-auto">
              {messages.map((msg, index) => (
                <ChatMessage
                  key={index}
                  message={msg.text}
                  isUser={msg.isUser}
                />
              ))}
              {loading && (
                <div className="flex justify-start mb-4">
                  <div className="bg-gray-100 px-4 py-3 rounded-lg">
                    <div className="flex gap-1">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200"></div>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>

        <div className="bg-white">
          <div className="max-w-4xl mx-auto">
            <ChatInput onSend={handleSendMessage} disabled={loading} />
          </div>
        </div>
      </main>

      <footer className="bg-white border-t border-gray-200 py-3">
        <div className="max-w-6xl mx-auto px-4 text-center text-sm text-gray-600">
          Powered by Google Gemini • Built with React & FastAPI
        </div>
      </footer>
    </div>
  );
}

export default App;



