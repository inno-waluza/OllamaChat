
 # The bigest problem is each time it create a new interface of Ai i will fix it later
import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLabel,
    QPushButton,
    QTextEdit,
    QLineEdit,
    QComboBox,
    QMessageBox,
)
import re
import requests
import json
import pyttsx3
import threading


class ChatbotGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Ollama Chatbot")
        self.setFixedSize(600, 400)

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layouts
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Model Selection
        model_layout = QHBoxLayout()
        main_layout.addLayout(model_layout)

        model_label = QLabel("Select Model:")
        self.model_combo_box = QComboBox()
        self.model_combo_box.addItems(
            [
                "llama2-uncensored",
                "llama3",
                "phi3",
                "wizardlm2",
                "mistral",
                "gemma",
                "mixtral",
                "llama2",
                "Custom Model",
            ]
        )
        model_layout.addWidget(model_label)
        model_layout.addWidget(self.model_combo_box)

        # Text-to-Speech Option
        tts_layout = QHBoxLayout()
        main_layout.addLayout(tts_layout)

        self.tts_enabled = False
        tts_label = QLabel("Enable Text-to-Speech:")
        self.tts_checkbox = QPushButton("OFF")
        self.tts_checkbox.clicked.connect(self.toggle_tts)
        tts_layout.addWidget(tts_label)
        tts_layout.addWidget(self.tts_checkbox)

        # Real-time Output Option
        rto_layout = QHBoxLayout()
        main_layout.addLayout(rto_layout)

        self.rto_enabled = False
        rto_label = QLabel("Show Real-time Output:")
        self.rto_checkbox = QPushButton("Off")
        self.rto_checkbox.clicked.connect(self.toggle_rto)
        rto_layout.addWidget(rto_label)
        rto_layout.addWidget(self.rto_checkbox)

        # Chat Area
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        main_layout.addWidget(self.chat_area)

        # Input Box and Send Button
        input_layout = QHBoxLayout()
        main_layout.addLayout(input_layout)

        self.input_box = QLineEdit()
        input_layout.addWidget(self.input_box)

        send_button = QPushButton("Send")
        send_button.clicked.connect(self.send_message)
        input_layout.addWidget(send_button)

        # Initialize Variables
        self.selected_model = "llama3"

    def toggle_tts(self):
        if self.tts_enabled:
            self.tts_enabled = False
            self.tts_checkbox.setText("OFF")
        else:
            self.tts_enabled = True
            self.tts_checkbox.setText("ON")

    def toggle_rto(self):
        if self.rto_enabled:
            self.rto_enabled = False
            self.rto_checkbox.setText("OFF")
        else:
            self.rto_enabled = True
            self.rto_checkbox.setText("ON")

    def display_message(self, role, message):
        self.chat_area.append(f"{role}: {message}")

    def send_message(self):
        user_input = self.input_box.text()
        if user_input.lower() == "exit":
            self.display_message("System", "Exiting...")
            sys.exit()

        # Send user's message to the server with the selected model
        assistant_response = send_message(
            user_input, self.selected_model, self.rto_enabled, self
        )

        # Display the assistant's response in the chat area
        self.display_message("Assistant", assistant_response)

        # Convert the assistant's response to speech if enabled
        if self.tts_enabled:
            threading.Thread(target=text_to_speech, args=(assistant_response,)).start()

        # Clear input box
        self.input_box.clear()

    def start_chat(self):
        self.selected_model = self.model_combo_box.currentText()
        self.display_message("System", "Chat started with model: " + self.selected_model)


def send_message(message, model, real_time_output_enabled=True, window=None):
    # Define the endpoint URL
    url = "http://localhost:11434/api/chat"

    # Define the payload (data) to be sent in the request
    data = {
        "model": model,
        "messages": [{"role": "user", "content": message}],
    }

    # Send the POST request to the API endpoint with streaming enabled
    response = requests.post(url, json=data, stream=True)

    # Initialize response data
    response_data = ""

    # Buffer to store assistant's responses for the current sentence
    sentence_buffer = []

    # Iterate over the streaming response
    for line in response.iter_lines():
        if line:
            # Parse the JSON line
            json_line = json.loads(line)
            # Extract the assistant's response
            assistant_response = json_line["message"]["content"]

            # Ensure the assistant's response is properly formatted
            assistant_response = assistant_response.strip()

            response_data += assistant_response + " "

            # Check if it's the final response
            if json_line.get("done"):
                break

            # Add assistant's response to the buffer
            sentence_buffer.append(assistant_response)

            # Check if the assistant's response ends with punctuation indicating the end of a sentence
            if assistant_response.endswith((".", "!", "?")):
                # Print the buffered responses if real-time output is enabled
                if real_time_output_enabled:
                    window.display_message(
                        "Assistant", " ".join(sentence_buffer)
                    )
                sentence_buffer = []

    return response_data.strip()


def text_to_speech(text):
    # Initialize the TTS engine
    engine = pyttsx3.init()
    # Convert text to speech
    engine.say(text)

    # Wait for the speech to finish
    engine.runAndWait()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    chat_window = ChatbotGUI()
    chat_window.show()
    sys.exit(app.exec())
