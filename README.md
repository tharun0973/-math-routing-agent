# Math Routing Agent

A modern, AI-powered mathematics assistant built with React and Tailwind CSS.

## Features

- 🎨 Beautiful dark-themed UI
- 📱 Responsive design
- 🧮 Math problem solving interface
- 💬 Chat history tracking
- ⚡ Fast performance with Vite

## Tech Stack

- **React** ^18.2.0 - UI framework
- **Tailwind CSS** ^3.3.2 - Utility-first styling
- **React Icons** ^4.10.1 - Icon library
- **Framer Motion** ^10.12.16 - Animations (optional)
- **React Router DOM** ^6.14.2 - Routing
- **Vite** - Build tool

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

3. Open your browser and navigate to `http://localhost:5173`

## Project Structure

```
math-routing-agent/
├── src/
│   ├── components/
│   │   ├── Sidebar.jsx       # Chat history sidebar
│   │   └── MainContent.jsx   # Main chat interface
│   ├── App.jsx               # Main app component
│   ├── index.css             # Global styles
│   └── main.jsx              # Entry point
├── tailwind.config.js        # Tailwind configuration
└── package.json
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Customization

### Colors

Edit `tailwind.config.js` to customize the color scheme:

```javascript
colors: {
  primary: {
    dark: '#1A1A1A',      // Sidebar background
    darker: '#121212',    // Main background
    orange: '#FF6B35',    // Primary accent
    'orange-hover': '#E55A2B', // Hover state
  },
}
```

## License

MIT
