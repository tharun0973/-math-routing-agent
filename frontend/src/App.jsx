import { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import MainContent from './components/MainContent';

function App() {
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const saved = localStorage.getItem('mathChatHistory');
    if (saved) {
      setChatHistory(JSON.parse(saved));
    }
  }, []);

  useEffect(() => {
    localStorage.setItem('mathChatHistory', JSON.stringify(chatHistory));
  }, [chatHistory]);

  const handleNewChat = () => {
    setChatHistory([]);
  };

  const handleSendMessage = async (question) => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/solve', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question }),
      });

      const data = await response.json();
      const newChat = {
        question,
        answer: data.answer,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setChatHistory(prev => [...prev, newChat]);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen w-screen overflow-hidden">
      <Sidebar chatHistory={chatHistory} onNewChat={handleNewChat} />
      <MainContent onSendMessage={handleSendMessage} loading={loading} />
    </div>
  );
}

export default App;
