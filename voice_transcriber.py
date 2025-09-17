"""
Voice Transcription System with Semantic Decision Tree Generation

This module provides real-time voice transcription and creates semantic decision trees
from conversations using local Llama 3.2 model via Ollama.
"""

import speech_recognition as sr
import requests
import json
import time
import threading
from datetime import datetime
from typing import List, Dict, Any, Optional
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict, deque


class VoiceTranscriber:
    """Real-time voice transcription system."""
    
    def __init__(self, ollama_url: str = "http://localhost:11434"):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.ollama_url = ollama_url
        self.is_listening = False
        self.transcription_buffer = []
        self.semantic_chunks = []
        self.decision_tree = nx.DiGraph()
        
        # Initialize sentence transformer for semantic similarity
        self.sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Calibrate microphone
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
        
        print("Voice transcriber initialized. Microphone calibrated.")
    
    def transcribe_audio(self, audio_data) -> Optional[str]:
        """Transcribe audio data to text."""
        try:
            # Use Google's speech recognition (free tier)
            text = self.recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from speech recognition service; {e}")
            return None
    
    def start_listening(self):
        """Start continuous voice transcription."""
        self.is_listening = True
        print("🎤 Started listening... Speak now!")
        
        def listen_continuously():
            with self.microphone as source:
                while self.is_listening:
                    try:
                        # Listen for audio with timeout
                        audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                        text = self.transcribe_audio(audio)
                        
                        if text:
                            timestamp = datetime.now()
                            self.transcription_buffer.append({
                                'text': text,
                                'timestamp': timestamp,
                                'id': len(self.transcription_buffer)
                            })
                            print(f"📝 [{timestamp.strftime('%H:%M:%S')}] {text}")
                            
                            # Process for semantic chunking
                            self.process_semantic_chunking()
                            
                    except sr.WaitTimeoutError:
                        continue
                    except Exception as e:
                        print(f"Error in listening: {e}")
                        continue
        
        # Start listening in a separate thread
        self.listen_thread = threading.Thread(target=listen_continuously, daemon=True)
        self.listen_thread.start()
    
    def stop_listening(self):
        """Stop voice transcription."""
        self.is_listening = False
        print("🛑 Stopped listening.")
    
    def process_semantic_chunking(self):
        """Group transcription segments into semantic chunks."""
        if len(self.transcription_buffer) < 2:
            return
        
        # Get recent transcriptions
        recent_transcripts = self.transcription_buffer[-10:]  # Last 10 segments
        texts = [item['text'] for item in recent_transcripts]
        
        if len(texts) < 2:
            return
        
        # Generate embeddings
        embeddings = self.sentence_model.encode(texts)
        
        # Calculate similarity matrix
        similarity_matrix = cosine_similarity(embeddings)
        
        # Simple clustering based on similarity threshold
        threshold = 0.7
        chunks = []
        current_chunk = [recent_transcripts[0]]
        
        for i in range(1, len(recent_transcripts)):
            if similarity_matrix[i-1][i] > threshold:
                current_chunk.append(recent_transcripts[i])
            else:
                if len(current_chunk) > 1:
                    chunks.append(current_chunk)
                current_chunk = [recent_transcripts[i]]
        
        if len(current_chunk) > 1:
            chunks.append(current_chunk)
        
        # Update semantic chunks
        for chunk in chunks:
            chunk_text = " ".join([item['text'] for item in chunk])
            chunk_id = f"chunk_{len(self.semantic_chunks)}"
            
            self.semantic_chunks.append({
                'id': chunk_id,
                'text': chunk_text,
                'segments': chunk,
                'timestamp': chunk[0]['timestamp'],
                'embedding': self.sentence_model.encode([chunk_text])[0]
            })
            
            print(f"🧩 New semantic chunk: {chunk_text[:100]}...")
            
            # Generate decision tree nodes
            self.generate_decision_tree_node(chunk_text, chunk_id)
    
    def generate_decision_tree_node(self, text: str, chunk_id: str):
        """Generate decision tree nodes using Llama."""
        try:
            # Create prompt for Llama to analyze the conversation chunk
            prompt = f"""
            Analyze this conversation segment and identify:
            1. Main topic or decision point
            2. Key options or choices mentioned
            3. Context or reasoning
            4. Next logical steps or outcomes
            
            Conversation segment: "{text}"
            
            Respond in JSON format:
            {{
                "topic": "main topic",
                "decision_point": "key decision or choice",
                "options": ["option1", "option2"],
                "context": "background context",
                "next_steps": ["step1", "step2"]
            }}
            """
            
            # Call Ollama API
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": "llama3.2:3b",
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                analysis = result.get('response', '')
                
                # Try to extract JSON from response
                try:
                    # Find JSON in the response
                    start_idx = analysis.find('{')
                    end_idx = analysis.rfind('}') + 1
                    if start_idx != -1 and end_idx != -1:
                        json_str = analysis[start_idx:end_idx]
                        analysis_data = json.loads(json_str)
                    else:
                        # Fallback if no JSON found
                        analysis_data = {
                            "topic": "General Discussion",
                            "decision_point": "Topic Discussion",
                            "options": ["Continue", "Explore Further"],
                            "context": text[:100],
                            "next_steps": ["Continue conversation"]
                        }
                except json.JSONDecodeError:
                    # Fallback parsing
                    analysis_data = {
                        "topic": "General Discussion",
                        "decision_point": "Topic Discussion", 
                        "options": ["Continue", "Explore Further"],
                        "context": text[:100],
                        "next_steps": ["Continue conversation"]
                    }
                
                # Add node to decision tree
                self.add_decision_tree_node(chunk_id, analysis_data, text)
                
        except Exception as e:
            print(f"Error generating decision tree node: {e}")
    
    def add_decision_tree_node(self, chunk_id: str, analysis: Dict[str, Any], original_text: str):
        """Add a node to the decision tree graph."""
        # Add main node
        self.decision_tree.add_node(
            chunk_id,
            topic=analysis.get('topic', 'Unknown'),
            decision_point=analysis.get('decision_point', 'General'),
            context=analysis.get('context', ''),
            original_text=original_text,
            timestamp=datetime.now()
        )
        
        # Add option nodes and edges
        options = analysis.get('options', [])
        for i, option in enumerate(options):
            option_id = f"{chunk_id}_option_{i}"
            self.decision_tree.add_node(
                option_id,
                type='option',
                text=option,
                parent=chunk_id
            )
            self.decision_tree.add_edge(chunk_id, option_id, label=option)
        
        # Connect to previous nodes if they exist
        if len(self.decision_tree.nodes()) > 1:
            # Find the most recent node (excluding current)
            recent_nodes = [n for n in self.decision_tree.nodes() if n != chunk_id]
            if recent_nodes:
                # Connect to the most recent node
                last_node = recent_nodes[-1]
                self.decision_tree.add_edge(last_node, chunk_id, type='follows')
        
        print(f"🌳 Added decision tree node: {analysis.get('topic', 'Unknown')}")
    
    def visualize_decision_tree(self, save_path: str = "decision_tree.png"):
        """Visualize the decision tree."""
        if not self.decision_tree.nodes():
            print("No decision tree nodes to visualize.")
            return
        
        plt.figure(figsize=(15, 10))
        pos = nx.spring_layout(self.decision_tree, k=3, iterations=50)
        
        # Draw nodes
        main_nodes = [n for n in self.decision_tree.nodes() if not n.endswith('_option_')]
        option_nodes = [n for n in self.decision_tree.nodes() if n.endswith('_option_')]
        
        nx.draw_networkx_nodes(
            self.decision_tree, pos, 
            nodelist=main_nodes,
            node_color='lightblue', 
            node_size=1000,
            alpha=0.8
        )
        
        nx.draw_networkx_nodes(
            self.decision_tree, pos,
            nodelist=option_nodes,
            node_color='lightgreen',
            node_size=500,
            alpha=0.6
        )
        
        # Draw edges
        nx.draw_networkx_edges(self.decision_tree, pos, alpha=0.5, arrows=True)
        
        # Draw labels
        labels = {}
        for node in self.decision_tree.nodes():
            if node in main_nodes:
                topic = self.decision_tree.nodes[node].get('topic', 'Unknown')
                labels[node] = f"{node}\n{topic}"
            else:
                option_text = self.decision_tree.nodes[node].get('text', 'Option')
                labels[node] = option_text
        
        nx.draw_networkx_labels(self.decision_tree, pos, labels, font_size=8)
        
        plt.title("Conversation Decision Tree", fontsize=16, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"📊 Decision tree saved to {save_path}")
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get a summary of the conversation and decision tree."""
        return {
            'total_segments': len(self.transcription_buffer),
            'semantic_chunks': len(self.semantic_chunks),
            'decision_nodes': len([n for n in self.decision_tree.nodes() if not n.endswith('_option_')]),
            'option_nodes': len([n for n in self.decision_tree.nodes() if n.endswith('_option_')]),
            'transcription_buffer': self.transcription_buffer,
            'semantic_chunks': self.semantic_chunks,
            'decision_tree_nodes': list(self.decision_tree.nodes(data=True))
        }
    
    def save_conversation_data(self, filename: str = "conversation_data.json"):
        """Save conversation data to JSON file."""
        data = self.get_conversation_summary()
        
        # Convert datetime objects to strings for JSON serialization
        def convert_datetime(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            return obj
        
        # Convert the data
        json_data = json.loads(json.dumps(data, default=convert_datetime))
        
        with open(filename, 'w') as f:
            json.dump(json_data, f, indent=2)
        
        print(f"💾 Conversation data saved to {filename}")


def main():
    """Main function to run the voice transcription system."""
    print("🎯 Voice Transcription & Decision Tree System")
    print("=" * 50)
    
    # Initialize transcriber
    transcriber = VoiceTranscriber()
    
    try:
        # Start listening
        transcriber.start_listening()
        
        print("\nCommands:")
        print("- Press Enter to stop listening and visualize decision tree")
        print("- Type 'summary' to see conversation summary")
        print("- Type 'save' to save conversation data")
        print("- Type 'quit' to exit")
        
        while True:
            command = input("\n> ").strip().lower()
            
            if command == '':
                transcriber.stop_listening()
                print("\n📊 Generating decision tree visualization...")
                transcriber.visualize_decision_tree()
                break
            elif command == 'summary':
                summary = transcriber.get_conversation_summary()
                print(f"\n📈 Conversation Summary:")
                print(f"  - Total segments: {summary['total_segments']}")
                print(f"  - Semantic chunks: {summary['semantic_chunks']}")
                print(f"  - Decision nodes: {summary['decision_nodes']}")
                print(f"  - Option nodes: {summary['option_nodes']}")
            elif command == 'save':
                transcriber.save_conversation_data()
            elif command == 'quit':
                transcriber.stop_listening()
                break
            else:
                print("Unknown command. Try: summary, save, or just press Enter to stop.")
    
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        transcriber.stop_listening()
    except Exception as e:
        print(f"Error: {e}")
        transcriber.stop_listening()


if __name__ == "__main__":
    main()
