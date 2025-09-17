# 🎤 Voice Decision Tree - Web App

A beautiful, modern web interface for real-time voice transcription and decision tree generation using local Llama 3.2.

## ✨ Features

- 🎨 **Beautiful Modern UI** - No more ugly Python interfaces!
- 🎤 **Real-time Voice Recording** - Uses Web Speech API
- 🧠 **AI-Powered Analysis** - Local Llama 3.2 via Ollama
- 🌳 **Interactive Decision Trees** - Visual conversation flow
- 📊 **Live Statistics** - Real-time metrics
- 🚀 **Zero Setup** - Just run and go!

## 🚀 Quick Start

### Option 1: One-Command Start
```bash
./start.sh
```

### Option 2: Manual Start
```bash
# Make sure Ollama is running
brew services start ollama

# Start the web server
python3 server.py
```

### Option 3: Direct Browser
```bash
# Just open the HTML file directly in your browser
open index.html
```

## 🎯 How to Use

1. **Open your browser** to `http://localhost:8000`
2. **Click the microphone button** to start recording
3. **Speak your thoughts** - watch real-time transcription
4. **Click "Analyze"** to generate decision tree
5. **View your conversation flow** as a beautiful tree

## 🎨 What You Get

### Beautiful Interface
- Modern gradient backgrounds
- Smooth animations and transitions
- Responsive design (works on mobile too!)
- Clean, professional look

### Real-time Features
- Live voice transcription
- Instant visual feedback
- Progressive decision tree building
- Live statistics updates

### Smart Analysis
- Semantic understanding via Llama 3.2
- Automatic decision point detection
- Option extraction
- Context-aware analysis

## 🛠️ Technical Details

### Architecture
```
Browser → Web Speech API → Local Server → Ollama API → Beautiful UI
```

### Technologies
- **Frontend**: Pure HTML/CSS/JavaScript (no frameworks!)
- **Voice**: Web Speech API (built into browsers)
- **AI**: Local Llama 3.2 via Ollama
- **Server**: Simple Python HTTP server
- **No databases** - everything in memory

### Browser Compatibility
- ✅ Chrome/Chromium (best support)
- ✅ Safari (good support)
- ✅ Firefox (good support)
- ✅ Edge (good support)

## 🎛️ Customization

### Styling
Edit the CSS in `index.html` to customize:
- Colors and gradients
- Fonts and typography
- Layout and spacing
- Animations and effects

### Analysis
Modify the prompt in the JavaScript to change how Llama analyzes conversations:
```javascript
const prompt = `Your custom analysis prompt here...`;
```

### Voice Settings
Adjust speech recognition settings:
```javascript
this.recognition.lang = 'en-US';  // Change language
this.recognition.continuous = true;  // Continuous listening
```

## 🔧 Troubleshooting

### "Speech recognition not supported"
- Use Chrome or Safari (best support)
- Make sure you're on HTTPS or localhost
- Check microphone permissions

### "Ollama API error"
- Make sure Ollama is running: `brew services start ollama`
- Check if llama3.2:3b is installed: `ollama list`
- Try pulling the model: `ollama pull llama3.2:3b`

### "CORS error"
- Use the Python server (`python3 server.py`) instead of opening HTML directly
- The server handles CORS for Ollama API calls

### Microphone not working
- Check browser permissions
- Make sure no other apps are using the microphone
- Try refreshing the page

## 🎨 Screenshots

The interface features:
- **Gradient background** with modern design
- **Large record button** with pulse animation
- **Real-time transcription** area
- **Interactive decision tree** visualization
- **Live statistics** cards
- **Responsive layout** for all devices

## 🚀 Future Enhancements

- [ ] Multiple conversation sessions
- [ ] Export to PNG/PDF
- [ ] Custom analysis prompts
- [ ] Multi-language support
- [ ] Voice commands
- [ ] Conversation history
- [ ] Collaborative features

## 📝 License

MIT License - feel free to modify and use!

## 🤝 Contributing

1. Fork the repository
2. Make your changes
3. Test thoroughly
4. Submit a pull request

---

**Enjoy your beautiful voice decision tree app!** 🎉
