#!/bin/bash
echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "🚀 Launching chatbot UI..."
python ollama_chatbot1.py

