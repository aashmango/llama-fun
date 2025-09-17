# Voice Decision Tree - Live Conversation Analysis

A real-time voice transcription and conversation analysis tool that creates visual representations of your speech patterns using AI.

## 🎯 Features

### **Dual Graph System**
- **Linear Transcription Graph** (Top): Shows conversation flow left-to-right with break annotations
- **Live Theme Mind Map** (Bottom): Clusters related themes using force-directed layout

### **Live Voice Processing**
- **Continuous Recording**: Auto-restart prevents random stops
- **Real-time Transcription**: Large, prominent live text display
- **Smart Break Detection**: Creates nodes on pauses, transition words, and sentence endings
- **Break Annotations**: Shows what triggered each node ("but", "and", "pause", etc.)

### **AI-Powered Analysis**
- **Theme Extraction**: Uses Llama 3.2 3B to extract 1-3 word themes
- **Semantic Clustering**: Groups similar themes using word similarity
- **Force-Directed Layout**: Physics-based positioning prevents overlaps
- **Strength Scaling**: Popular themes grow larger and more prominent

## 🚀 Quick Start

### Prerequisites
- **Ollama** installed with Llama 3.2 3B model
- **Python 3.9+**
- **Modern web browser** with speech recognition support

### Installation

1. **Install Ollama and download Llama 3.2**:
   ```bash
   # Install Ollama (macOS)
   brew install ollama
   
   # Download Llama 3.2 3B model
   ollama pull llama3.2:3b
   ```

2. **Install Python dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Start the server**:
   ```bash
   python3 server.py
   ```

4. **Open in browser**:
   ```
   http://localhost:8080
   ```

## 🎮 Usage

1. **Start Recording**: Click the record button (turns red when active)
2. **Speak Naturally**: See live transcription in large text at bottom
3. **Watch Graphs Build**:
   - Top: Linear conversation flow with break annotations
   - Bottom: Theme clusters forming automatically
4. **Stop Recording**: Click the button again to stop

## 🧠 How It Works

### **Voice Processing Pipeline**
```
Speech → Browser Speech API → Break Detection → Node Creation → Graph Layout
```

### **Theme Analysis Pipeline**
```
Transcription → Buffer (5s) → Llama 3.2 Analysis → Theme Extraction → Clustering → Force Layout
```

### **Clustering Algorithm**
- **Similarity Calculation**: Word overlap between themes
- **Attraction Forces**: Similar themes (>30% similarity) cluster together
- **Repulsion Forces**: Different themes maintain 120px minimum distance
- **Physics Simulation**: 100 iterations per new theme addition

## 📁 Project Structure

```
llama-fun/
├── index.html          # Main web application
├── server.py           # Local HTTP server with CORS
├── requirements.txt    # Python dependencies
├── start.sh           # Quick start script
└── README.md          # This file
```

## 🔧 Configuration

### **Speech Recognition Settings**
- **Continuous**: Never stops automatically
- **Interim Results**: Shows live transcription
- **Auto-restart**: Handles network/timeout issues
- **Language**: English (US)

### **Theme Analysis Settings**
- **Analysis Interval**: Every 5 seconds
- **Similarity Threshold**: 30% for clustering, 70% for duplicates
- **Force Layout**: 100 iterations, 0.9 damping
- **Node Spacing**: 80px target, 120px minimum

### **Break Detection Triggers**
- **Transition words**: "but", "and", "if", "however", "so", "then", etc.
- **Sentence endings**: Periods, exclamation marks, question marks
- **Pauses**: 2+ seconds of silence

## 🎨 Visual Design

### **Node Types**
- **Transcription Nodes**: White rectangles with clean text
- **Theme Nodes**: Green pills with 1-3 word phrases
- **Connection Lines**: Gray lines with break word annotations

### **Layout Patterns**
- **Linear Flow**: 3-row staggered pattern, left-to-right
- **Mind Map**: Organic clustering around canvas center
- **Force Physics**: Smooth, natural positioning

## 🔍 Troubleshooting

### **Recording Stops Randomly**
- Auto-restart should handle this automatically
- Check browser console for restart messages
- Ensure microphone permissions are granted

### **No Themes Appearing**
- Verify Ollama is running: `ollama list`
- Check server console for API errors
- Ensure Llama 3.2 model is downloaded

### **Overlapping Nodes**
- Force-directed layout should prevent this
- Try clearing and restarting if issues persist
- Check browser console for layout errors

## 🛠 Development

### **Local Development**
```bash
# Start Ollama service
ollama serve

# Start local server
python3 server.py

# Open browser to localhost:8080
```

### **Customization**
- **Themes**: Modify LLM prompt in `extractThemes()`
- **Layout**: Adjust force parameters in `runForceDirectedLayout()`
- **Styling**: Edit CSS in `index.html`
- **Break Detection**: Modify regex in `checkForNaturalBreaks()`

## 📊 Technical Details

### **Dependencies**
- **Frontend**: Vanilla JavaScript, HTML5 Speech API
- **Backend**: Python HTTP server, Ollama API
- **AI Model**: Meta Llama 3.2 3B (via Ollama)
- **Physics**: Custom force-directed layout algorithm

### **Browser Compatibility**
- **Chrome/Chromium**: Full support
- **Safari**: Full support  
- **Firefox**: Limited speech recognition support
- **Edge**: Full support

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- **Meta Llama 3.2** for theme analysis
- **Ollama** for local LLM hosting
- **Browser Speech API** for voice recognition
- **Force-directed graphs** inspiration from D3.js