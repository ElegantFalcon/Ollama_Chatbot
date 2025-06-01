#!/bin/bash
echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "🚀 Launching chatbot UI..."
python chatbot_with_sidebar.py

chmod +x run.sh
