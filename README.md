# Ollama Chatbot

Ollama Chatbot is a conversational agent powered by AI that allows users to interact with an AI assistant through either a graphical user interface (GUI) or a console interface.

## Features

- **Graphical User Interface (GUI):** Provides a user-friendly interface for interacting with the AI assistant.
- **Console Interface:** Allows interaction with the AI assistant through the command line interface.

## AI Models

The AI models used in this chatbot are provided by Mistral AI or Ollama AI. The available models are:

- **Llama2:** A pre-trained AI model for conversation.
- **Llama2-Uncensored:** A variant of the Llama2 model without content filtering.

These models can be installed locally on a machine capable of running AI models.

## Requirements

- Python 3.x
- Required Python libraries:
  - Kivy==2.0.0
  - kivy-deps.angle==0.3.3
  - kivy-deps.glew==0.3.1
  - kivy-deps.sdl2==0.3.1
  - Kivy-Garden==0.1.5
  - kivymd==0.104.2
  - PySide6==6.7.0
  - PySide6_Addons==6.7.0
  - PySide6_Essentials==6.7.0
  - pyttsx3==2.90
  - requests==2.26.0

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/innowaluza/ollama-chatbot.git
    ```

2. Install the required Python libraries:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Graphical User Interface (GUI)

1. Run the `Ollamachat_GUI.py` script:

    ```bash
    python Ollamachat_GUI.py
    ```

2. Type your message in the input field and press "Send" to receive responses from the AI assistant.

### Console Interface

1. Run the `Ollamachat_console.py` script:

    ```bash
    python Ollamachat_console.py
    ```

2. Type your message in the console and press Enter to send it to the AI assistant. Type "exit" to end the conversation.

## Contributors

- [Innocent Waluza](https://github.com/inno-waluza)
- [Krafi](https://gitlab.com/krafi)

## License

This project is licensed under the [MIT License](LICENSE).
