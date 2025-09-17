#!/usr/bin/env python3
"""
Simple web server for Voice Decision Tree app
Serves the HTML file and handles CORS for Ollama API calls
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from urllib.parse import urlparse, parse_qs
import json
import requests

class CORSHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'
        return super().do_GET()

    def do_POST(self):
        if self.path == '/api/ollama':
            self.handle_ollama_proxy()
        else:
            self.send_error(404)

    def handle_ollama_proxy(self):
        """Proxy requests to Ollama to handle CORS"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Forward request to Ollama
            response = requests.post(
                'http://localhost:11434/api/generate',
                data=post_data,
                headers={'Content-Type': 'application/json'},
                timeout=60
            )
            
            self.send_response(response.status_code)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(response.content)
            
        except Exception as e:
            self.send_error(500, f"Ollama proxy error: {str(e)}")

def check_ollama():
    """Check if Ollama is running"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama is running!")
            return True
    except:
        pass
    
    print("❌ Ollama is not running. Please start it with:")
    print("   brew services start ollama")
    print("   ollama pull llama3.2:3b")
    return False

def main():
    """Start the web server"""
    print("🚀 Starting Voice Decision Tree Web App")
    print("=" * 50)
    
    # Check if Ollama is running
    if not check_ollama():
        sys.exit(1)
    
    # Set up server
    PORT = 8080
    
    # Change to the directory containing the HTML file
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    with socketserver.TCPServer(("", PORT), CORSHTTPRequestHandler) as httpd:
        print(f"🌐 Server running at http://localhost:{PORT}")
        print("📱 Open your browser and navigate to the URL above")
        print("🎤 Click the microphone button to start recording")
        print("\nPress Ctrl+C to stop the server")
        
        # Try to open browser automatically
        try:
            webbrowser.open(f'http://localhost:{PORT}')
        except:
            pass
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 Server stopped. Goodbye!")

if __name__ == "__main__":
    main()
