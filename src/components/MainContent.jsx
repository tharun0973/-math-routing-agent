import { useState } from 'react';
import { IoMdSend } from 'react-icons/io';

const MainContent = () => {
  const [input, setInput] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/solve', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: input }),
      });

      const data = await response.json();
      setAnswer(data.answer);
      setInput('');
    } catch (error) {
      console.error('Error fetching solution:', error);
      setAnswer('Something went wrong. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !loading) {
      handleSend();
    }
  };

  return (
    <div className="flex-1 bg-primary-darker h-screen flex flex-col">
      <div className="flex-1 flex items-center justify-center">
        <div className="text-center max-w-2xl px-6">
          <h1 className="text-white text-4xl font-bold mb-4">
            Welcome to Math Routing Agent
          </h1>
          <p className="text-gray-400 text-lg leading-relaxed">
            Your AI-powered mathematics assistant. Get instant help with complex
            problems, step-by-step solutions, and personalized learning support.
          </p>
        </div>
      </div>

      <div className="p-6">
        <div className="max-w-4xl mx-auto">
          <div className="flex items-center gap-3">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask me any math question..."
              className="flex-1 bg-gray-700 text-white placeholder-gray-400 px-4 py-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-orange"
              disabled={loading}
            />
            <button
              onClick={handleSend}
              disabled={loading}
              className="bg-primary-orange hover:bg-primary-orange-hover text-white p-3 rounded-lg transition-colors shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <IoMdSend className="w-5 h-5" />
            </button>
          </div>

          {answer && (
            <div className="mt-6 bg-gray-800 text-white p-4 rounded-lg shadow">
              <p className="font-semibold mb-2">Answer:</p>
              <p>{answer}</p>
            </div>
          )}

          {loading && (
            <div className="mt-6 text-primary-orange text-center">
              <p>Solving your problem...</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MainContent;
