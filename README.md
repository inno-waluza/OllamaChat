# Ollama Chatbot

Ollama Chatbot is a conversational agent powered by AI that allows users to interact with an AI assistant through either a graphical user interface (GUI) or a console interface.

## Features

- **Graphical User Interface (GUI):** Provides a user-friendly interface for interacting with the AI assistant.
- **Console Interface:** Allows interaction with the AI assistant through the command line interface.

## Screenshots

### Graphical User Interface (GUI)

![GUI](/assets/GUI.png)

### Console Interface

![Console](/assets/console.png)


## AI Models

The AI models used in this chatbot are provided by Mistral AI or Ollama AI. The available models are:

- **Llama2:** A pre-trained AI model for conversation.
- **Llama2-Uncensored:** A variant of the Llama2 model without content filtering.

These models can be installed locally on a machine capable of running AI models.

## Requirements

- Python 3.x
- Required Python libraries:
  - Kivy
  - KivyMD
  - Requests
  - Pyttsx3

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

## License

This project is licensed under the [MIT License](LICENSE).
