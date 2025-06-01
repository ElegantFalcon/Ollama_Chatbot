#!/usr/bin/env python
# coding: utf-8

# In[18]:


import gradio as gr
import requests
import subprocess
import threading
import time


# In[19]:


OLLAMA_API_BASE = "http://localhost:11434"

def list_models():
    """Returns a list of installed models."""
    try:
        response = requests.get(f"{OLLAMA_API_BASE}/api/tags")
        response.raise_for_status()
        models = response.json().get("models", [])
        return [model["name"] for model in models]
    except Exception:
        return []

def list_available_models():
    """Static or dynamically fetched list of common/popular models to offer for download."""
    return [
        "llama2", "mistral", "gemma", "codellama", "orca-mini", 
        "phi", "dolphin-mixtral", "llava", "qwen", "tinyllama"
    ]


def is_model_installed(model_name):
    """Check if a model is already pulled locally."""
    return model_name in list_models()

def pull_model(model_name, progress_callback):
    """Pull a model using Ollama's API with progress updates."""
    try:
        response = requests.post(
            f"{OLLAMA_API_BASE}/api/pull",
            json={"name": model_name},
            stream=True
        )
        for line in response.iter_lines():
            if line:
                progress_callback(line.decode())
    except Exception as e:
        progress_callback(f"Error pulling model: {e}")


# In[20]:


chat_history = []
def chat_with_model(message, model_name, chat_history_state, progress=gr.Progress(track_tqdm=True)):
    if not is_model_installed(model_name):
        permission = gr.update(visible=True)
        return gr.update(value="Model not found locally. Please allow installation."), chat_history_state, permission

    # Append user message
    chat_history_state.append({"role": "user", "content": message})

    response = requests.post(
        f"{OLLAMA_API_BASE}/api/chat",
        json={
            "model": model_name,
            "messages": chat_history_state,
            "stream": False,
        }
    )
    reply = response.json()["message"]["content"]

    # Append assistant reply
    chat_history_state.append({"role": "assistant", "content": reply})

    formatted_history = []
    for i in range(0, len(chat_history_state), 2):
        user_msg = chat_history_state[i]["content"] if i < len(chat_history_state) else ""
        assistant_msg = chat_history_state[i+1]["content"] if i+1 < len(chat_history_state) else ""
        formatted_history.append([user_msg, assistant_msg])

    return formatted_history, chat_history_state, gr.update(visible=False)



# In[21]:


def install_model_ui(model_name):
    outputs = []
    def pull_callback(update):
        outputs.append(update)

    thread = threading.Thread(target=pull_model, args=(model_name, pull_callback))
    thread.start()
    while thread.is_alive():
        time.sleep(1)
        yield "\n".join(outputs)
    yield "\n".join(outputs)


# In[29]:


with gr.Blocks() as demo:
    gr.Markdown("## 💬 Chat with Ollama LLMs")

    with gr.Row():
        with gr.Column(scale=3):
            installed_models = list_models()
            all_known_models = list_available_models()
            models_to_download = sorted(list(set(all_known_models) - set(installed_models)))

            with gr.Row():
                installed_dropdown = gr.Dropdown(label="Installed Models", choices=installed_models, interactive=True)
                download_dropdown = gr.Dropdown(label="Available to Download", choices=models_to_download, interactive=True)

            chatbot = gr.Chatbot(label="Conversation", type="messages")
            msg = gr.Textbox(label="Your Message", placeholder="Type a message and press Enter")
            state = gr.State([])

            install_warning = gr.Textbox(value="Model not installed. Please install it first.", visible=False, interactive=False)
            install_button = gr.Button("Install Selected Model", visible=False)
            install_output = gr.Textbox(label="Installation Progress", lines=6, visible=True)

        with gr.Column(scale=1):
            gr.Markdown("### 📜 Chat History")

            chat_history_box = gr.Textbox(label="Raw History", lines=20, interactive=False, show_copy_button=True)

    def handle_user_input(user_message, selected_model, chat_state):
        if not is_model_installed(selected_model):
            return [], chat_state, gr.update(visible=True), ""

        # Append user message to state
        chat_state.append({"role": "user", "content": user_message})

        # Send request to Ollama
        try:
            response = requests.post(
                f"{OLLAMA_API_BASE}/api/chat",
                json={
                    "model": selected_model,
                    "messages": chat_state,
                    "stream": False
                }
            )
            reply = response.json()["message"]["content"]
        except Exception as e:
            reply = f"⚠️ Error: {str(e)}"

        # Append assistant's reply to state
        chat_state.append({"role": "assistant", "content": reply})

        # Format for gr.Chatbot (type="messages")
        chatbot_messages = [
            {"role": entry["role"], "content": entry["content"]} for entry in chat_state
        ]

        # Format for sidebar history
        readable_text = ""
        for i in range(0, len(chat_state), 2):
            user = chat_state[i]["content"]
            bot = chat_state[i + 1]["content"] if i + 1 < len(chat_state) else ""
            readable_text += f"👤: {user}\n🤖: {bot}\n\n"

        return chatbot_messages, chat_state, gr.update(visible=False), readable_text


    def on_model_select(selected_model):
        if not is_model_installed(selected_model):
            return gr.update(visible=True)
        return gr.update(visible=False)

    def refresh_model_lists():
        installed = list_models()
        all_known = list_available_models()
        not_installed = sorted(list(set(all_known) - set(installed)))
        return (
            gr.update(choices=installed),
            gr.update(choices=not_installed)
        )

    def install_model_ui(model_name):
        outputs = []
        def pull_callback(update):
            outputs.append(update)

        thread = threading.Thread(target=pull_model, args=(model_name, pull_callback))
        thread.start()
        while thread.is_alive():
            time.sleep(1)
            yield "\n".join(outputs)
        yield "\n".join(outputs)

    msg.submit(
    handle_user_input,
    inputs=[msg, installed_dropdown, state],
    outputs=[chatbot, state, install_button, chat_history_box]
    )


    download_dropdown.change(on_model_select, inputs=download_dropdown, outputs=install_button)
    install_button.click(install_model_ui, inputs=download_dropdown, outputs=install_output)

demo.launch()


if __name__ == "__main__":
    launch_interface()



# In[ ]:





# In[ ]:




