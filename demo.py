#!/usr/bin/env python3
"""
Demo script for Voice Transcription & Decision Tree System
This script demonstrates the system without requiring microphone access.
"""

import requests
import json
import time
from datetime import datetime
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
import matplotlib.pyplot as plt

def test_ollama_connection():
    """Test connection to Ollama."""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama is running!")
            return True
    except:
        pass
    
    print("❌ Ollama is not running. Please start it with: brew services start ollama")
    return False

def test_llama_inference():
    """Test Llama inference."""
    try:
        prompt = "Hello, can you help me understand how to create a voice transcription system?"
        
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:3b",
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Llama inference working!")
            print(f"Response: {result.get('response', '')[:200]}...")
            return True
        else:
            print(f"❌ Llama inference failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Llama inference error: {e}")
        return False

def test_semantic_analysis():
    """Test semantic analysis with sample conversation."""
    print("\n🧩 Testing semantic analysis...")
    
    # Sample conversation segments
    sample_conversation = [
        "I want to build a voice transcription system",
        "The system should work in real-time",
        "I need to process audio from a microphone",
        "The transcription should be accurate",
        "I want to group related conversation parts",
        "Semantic chunking would be useful",
        "I need to create decision trees from conversations",
        "The system should use local AI models",
        "Ollama with Llama would be perfect for this",
        "I want to visualize the conversation flow"
    ]
    
    # Initialize sentence transformer
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Generate embeddings
    embeddings = model.encode(sample_conversation)
    
    # Calculate similarity matrix
    similarity_matrix = cosine_similarity(embeddings)
    
    # Simple clustering based on similarity threshold
    threshold = 0.3
    chunks = []
    current_chunk = [sample_conversation[0]]
    
    for i in range(1, len(sample_conversation)):
        if similarity_matrix[i-1][i] > threshold:
            current_chunk.append(sample_conversation[i])
        else:
            if len(current_chunk) > 1:
                chunks.append(current_chunk)
            current_chunk = [sample_conversation[i]]
    
    if len(current_chunk) > 1:
        chunks.append(current_chunk)
    
    print(f"📊 Found {len(chunks)} semantic chunks:")
    for i, chunk in enumerate(chunks):
        print(f"  Chunk {i+1}: {chunk}")
    
    return chunks

def test_decision_tree_generation():
    """Test decision tree generation."""
    print("\n🌳 Testing decision tree generation...")
    
    # Create a sample decision tree
    G = nx.DiGraph()
    
    # Add nodes
    G.add_node("start", topic="Project Planning", decision_point="Choose Technology")
    G.add_node("option1", type="option", text="Use Cloud APIs")
    G.add_node("option2", type="option", text="Use Local Models")
    G.add_node("local_choice", topic="Local Implementation", decision_point="Select Model")
    G.add_node("option3", type="option", text="Llama 3.2")
    G.add_node("option4", type="option", text="Other Models")
    
    # Add edges
    G.add_edge("start", "option1", label="Cloud APIs")
    G.add_edge("start", "option2", label="Local Models")
    G.add_edge("option2", "local_choice", type="follows")
    G.add_edge("local_choice", "option3", label="Llama 3.2")
    G.add_edge("local_choice", "option4", label="Other Models")
    
    # Visualize
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, k=3, iterations=50)
    
    # Draw nodes
    main_nodes = [n for n in G.nodes() if not n.startswith('option')]
    option_nodes = [n for n in G.nodes() if n.startswith('option')]
    
    nx.draw_networkx_nodes(G, pos, nodelist=main_nodes, node_color='lightblue', node_size=1000, alpha=0.8)
    nx.draw_networkx_nodes(G, pos, nodelist=option_nodes, node_color='lightgreen', node_size=500, alpha=0.6)
    
    # Draw edges
    nx.draw_networkx_edges(G, pos, alpha=0.5, arrows=True)
    
    # Draw labels
    labels = {}
    for node in G.nodes():
        if node in main_nodes:
            topic = G.nodes[node].get('topic', 'Unknown')
            labels[node] = f"{node}\n{topic}"
        else:
            option_text = G.nodes[node].get('text', 'Option')
            labels[node] = option_text
    
    nx.draw_networkx_labels(G, pos, labels, font_size=8)
    
    plt.title("Sample Decision Tree", fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig("sample_decision_tree.png", dpi=300, bbox_inches='tight')
    plt.show()
    
    print("✅ Decision tree generated and saved as 'sample_decision_tree.png'")
    return G

def main():
    """Main demo function."""
    print("🎯 Voice Transcription & Decision Tree System - Demo")
    print("=" * 60)
    
    # Test Ollama connection
    if not test_ollama_connection():
        return
    
    # Test Llama inference
    if not test_llama_inference():
        return
    
    # Test semantic analysis
    chunks = test_semantic_analysis()
    
    # Test decision tree generation
    decision_tree = test_decision_tree_generation()
    
    print("\n🎉 Demo completed successfully!")
    print("\nNext steps:")
    print("1. Run 'python3 voice_transcriber.py' to start the full system")
    print("2. Make sure your microphone is connected and accessible")
    print("3. Speak into the microphone to see real-time transcription")
    print("4. Press Enter to generate decision tree visualization")

if __name__ == "__main__":
    main()
