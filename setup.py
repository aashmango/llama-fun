#!/usr/bin/env python3
"""
Setup script for Voice Transcription & Decision Tree System
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required Python packages."""
    print("📦 Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False
    return True

def check_ollama():
    """Check if Ollama is running."""
    print("🔍 Checking if Ollama is running...")
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama is running!")
            return True
    except:
        pass
    
    print("❌ Ollama is not running. Please start it with: brew services start ollama")
    return False

def check_microphone():
    """Check if microphone is available."""
    print("🎤 Checking microphone availability...")
    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        mic = sr.Microphone()
        with mic as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
        print("✅ Microphone is available!")
        return True
    except Exception as e:
        print(f"❌ Microphone error: {e}")
        return False

def main():
    """Main setup function."""
    print("🚀 Setting up Voice Transcription & Decision Tree System")
    print("=" * 60)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        sys.exit(1)
    
    print(f"✅ Python {sys.version.split()[0]} detected")
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Check Ollama
    if not check_ollama():
        print("\n💡 To start Ollama:")
        print("   brew services start ollama")
        print("   ollama pull llama3.2:3b")
        sys.exit(1)
    
    # Check microphone
    if not check_microphone():
        print("\n💡 Make sure your microphone is connected and not being used by other applications.")
        sys.exit(1)
    
    print("\n🎉 Setup complete! You can now run:")
    print("   python3 voice_transcriber.py")

if __name__ == "__main__":
    main()
