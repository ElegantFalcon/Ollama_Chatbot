🧠 Local LLM Chatbot Interface with Gradio + Ollama

This project provides an interactive chatbot UI built with Gradio, using locally hosted LLMs via Ollama.
✨ Features

    🔄 Dropdowns to switch models

        Installed models

        Downloadable models (with install prompt and progress)

    💬 Chatbot UI 
    🧾 Sidebar with live chat history

    ✅ No cloud dependency — works fully locally

🚀 Getting Started
1. Install Requirements

pip install gradio requests

Make sure Ollama is installed and running locally:

ollama serve

2. Run the Notebook

Launch the Jupyter notebook:

jupyter notebook

Open chatbot_with_sidebar.ipynb and run all cells.
🧪 Available Models

This UI automatically lists:

    ✅ Installed Models (via ollama list)

    ⬇️ Available Models to Download (from ollama.com/library)

When selecting a model not installed locally, you'll be prompted to install it with live progress.
🛠 Tech Stack
Tool	Purpose
Gradio	Frontend chatbot UI
Ollama	Local model server
Python	Backend logic
requests	To interact with Ollama API
📁 File Structure

📦 ollama-chatbot
 ┣ 🧠 chatbot_with_sidebar.ipynb   # Main notebook
 ┣ 📄 README.md                    # This file
 ┗ requirements.txt               # Optional, for pip installs

✅ Example LLMs You Can Use

    llama3

    mistral

    gemma

    codellama

    neural-chat

Check Ollama's model library for full list.
