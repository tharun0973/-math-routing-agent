import { useState } from 'react';
import { IoMdSend } from 'react-icons/io';
import { FiUpload } from 'react-icons/fi';

const MainContent = ({ onSendMessage, loading }) => {
  const [input, setInput] = useState('');
  const [answer, setAnswer] = useState('');

  const handleSend = () => {
    if (!input.trim() || loading) return;
    onSendMessage(input);
    setAnswer('');
    setInput('');
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !loading) {
      handleSend();
    }
  };

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      console.log('Uploading file:', file.name);
      // Add your file upload logic here
    }
  };

  return (
    <div className="flex-1 flex flex-col bg-primary-darker h-screen">
      {/* Welcome Section */}
      <div className="flex-1 flex flex-col items-center justify-center text-center px-6">
        <h1 className="text-white text-4xl font-bold mb-4">
          Welcome to Math Routing Agent
        </h1>
        <p className="text-gray-400 text-lg leading-relaxed max-w-2xl">
          Your AI-powered mathematics assistant. Get instant help with complex
          problems, step-by-step solutions, and personalized learning support.
        </p>

        {/* Curved Chat Bar */}
        <div className="mt-10 flex justify-center">
          <div className="w-[720px] bg-gray-800 border border-primary-orange rounded-full flex items-center px-5 py-3 shadow-lg gap-4">
            {/* Upload Button */}
            <label className="cursor-pointer text-white hover:text-primary-orange transition-colors">
              <FiUpload className="w-5 h-5" />
              <input
                type="file"
                className="hidden"
                accept=".pdf,.jpg,.jpeg,.png,.txt"
                onChange={handleFileUpload}
              />
            </label>

            {/* Input Field */}
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask me any math question..."
              className="flex-1 bg-transparent text-white placeholder-gray-400 focus:outline-none"
              disabled={loading}
            />

            {/* Send Button */}
            <button
              onClick={handleSend}
              disabled={loading}
              className="bg-primary-orange hover:bg-primary-orange-hover text-white p-2 rounded-full transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <IoMdSend className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>

      {/* Answer Display */}
      {answer && (
        <div className="pb-8 px-6 max-w-3xl mx-auto">
          <div className="mt-6 bg-gray-800 text-white p-4 rounded-lg shadow">
            <p className="font-semibold mb-2">Answer:</p>
            <p>{answer}</p>
          </div>
        </div>
      )}

      {/* Loading Message */}
      {loading && (
        <div className="pb-8 text-primary-orange text-center">
          <p>Solving your problem...</p>
        </div>
      )}
    </div>
  );
};

export default MainContent;
