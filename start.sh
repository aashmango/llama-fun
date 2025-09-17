#!/bin/bash

echo "🎯 Voice Decision Tree - Web App"
echo "================================="

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "❌ Ollama is not running. Starting it now..."
    brew services start ollama
    sleep 3
    
    # Check if llama3.2:3b is available
    if ! ollama list | grep -q "llama3.2:3b"; then
        echo "📥 Downloading Llama 3.2 3B model..."
        ollama pull llama3.2:3b
    fi
fi

echo "✅ Ollama is ready!"
echo "🚀 Starting web server..."

# Start the web server
python3 server.py
