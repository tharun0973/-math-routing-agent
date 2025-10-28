import { FiPlus } from 'react-icons/fi';

const Sidebar = () => {
  const todayChats = [
    { title: 'Quadratic Formula Help', time: '2:30 PM' },
    { title: 'Derivative Calculations', time: '11:45 AM' },
    { title: 'Matrix Operations', time: '9:15 AM' },
  ];

  const yesterdayChats = [
    { title: 'Probability Distribution', time: '6:20 PM' },
    { title: 'Trigonometry Identities', time: '3:45 PM' },
  ];

  const thisWeekChats = [
    { title: 'Complex Numbers', time: 'Monday 4:30 PM' },
    { title: 'Linear Algebra Basics', time: 'Sunday 2:15 PM' },
  ];

  const ChatSection = ({ label, chats }) => (
    <div className="mb-8">
      <h3 className="text-gray-400 text-xs uppercase tracking-wider mb-3 px-6">
        {label}
      </h3>
      <div className="space-y-1">
        {chats.map((chat, index) => (
          <div
            key={index}
            className="px-6 py-2 hover:bg-gray-800 cursor-pointer transition-colors"
          >
            <p className="text-white text-sm font-medium">{chat.title}</p>
            <p className="text-gray-500 text-xs mt-1">{chat.time}</p>
          </div>
        ))}
      </div>
    </div>
  );

  return (
    <div className="w-1/4 bg-primary-dark h-screen flex flex-col">
      {/* New Chat Button */}
      <div className="p-6">
        <button className="w-full bg-primary-orange hover:bg-primary-orange-hover text-white font-semibold py-3 px-4 rounded-lg transition-colors shadow-lg flex items-center justify-center gap-2">
          <FiPlus className="w-5 h-5" />
          New Chat
        </button>
      </div>

      {/* Chat History */}
      <div className="flex-1 overflow-y-auto">
        <ChatSection label="TODAY" chats={todayChats} />
        <ChatSection label="YESTERDAY" chats={yesterdayChats} />
        <ChatSection label="THIS WEEK" chats={thisWeekChats} />
      </div>

      {/* Agent Profile */}
      <div className="border-t border-gray-700 p-6">
        <p className="text-white font-semibold">Math Routing Agent</p>
        <p className="text-gray-400 text-sm mt-1">AI Math Assistant</p>
      </div>
    </div>
  );
};

export default Sidebar;
