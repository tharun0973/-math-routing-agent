import { useState } from 'react';
import { IoMdSend } from 'react-icons/io';

const MainContent = () => {
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (input.trim()) {
      console.log('Sending:', input);
      setInput('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSend();
    }
  };

  return (
    <div className="flex-1 bg-primary-darker h-screen flex flex-col">
      {/* Welcome Section */}
      <div className="flex-1 flex items-center justify-center">
        <div className="text-center max-w-2xl px-6">
          <h1 className="text-white text-4xl font-bold mb-4">
            Welcome to Math Routing Agent
          </h1>
          <p className="text-gray-400 text-lg leading-relaxed">
            Your AI-powered mathematics assistant. Get instant help with complex
            problems, step-by-step solutions, and personalized learning support.
          </p>

          {/* Suggested Prompt */}
          <div className="mt-12 text-left">
            <div className="border border-primary-orange rounded-lg p-4 bg-primary-dark hover:bg-gray-800 cursor-pointer transition-colors">
              <p className="text-white text-base">
                Can you help me solve this quadratic equation: 3x² - 7x + 2 = 0?
              </p>
              <p className="text-gray-500 text-xs mt-2">Math Routing Agent</p>
            </div>
          </div>
        </div>
      </div>

      {/* Input Section */}
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
            />
            <button
              onClick={handleSend}
              className="bg-primary-orange hover:bg-primary-orange-hover text-white p-3 rounded-lg transition-colors shadow-lg"
            >
              <IoMdSend className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MainContent;
