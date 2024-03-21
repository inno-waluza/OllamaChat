import threading
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFlatButton
import requests
import json
import pyttsx3

# Load KivyMD design string
kv_string = '''
BoxLayout:
  orientation: 'vertical'
  padding: dp(20)

  BoxLayout:
    orientation: 'horizontal'
    size_hint_y: None
    height: self.minimum_height

    MDTextField:
      id: prompt_field
      hint_text: "Type your message"
      mode: "fill"
      fill_color: app.theme_cls.primary_color
      hint_text_color: [1, 1, 1, 0.7]
      on_text_validate: app.send_message()

    MDFlatButton:
      text: "Send"
      on_press: app.send_message()

  MDTextField:
    id: response_field
    hint_text: "AI Response"
    mode: "fill"
    fill_color: app.theme_cls.primary_color
    hint_text_color: [1, 1, 1, 0.7]
    readonly: True
'''

class ChatApp(MDApp):
  def build(self):
    self.theme_cls.theme_style = "Dark"
    self.title = "Ollama Chatbot"
    return Builder.load_string(kv_string)

  def send_message(self):
    def process_message_in_thread():
      user_input = self.root.ids.prompt_field.text

      # Define the endpoint URL
      url = "http://localhost:11434/api/chat"

      # Define the payload (data) to be sent in the request
      data = {
        "model": "llama2-uncensored",
        "messages": [
          {"role": "user", "content": user_input}
        ]
      }

      # Send the POST request to the API endpoint with streaming enabled
      response = requests.post(url, json=data, stream=True)

      # Initialize response data
      response_data = ""

      # Iterate over the streaming response
      for line in response.iter_lines():
        if line:
          # Parse the JSON line
          json_line = json.loads(line)
          # Extract the assistant's response
          assistant_response = json_line['message']['content']

          # Ensure the assistant's response is properly formatted
          assistant_response = assistant_response.strip()

          response_data += assistant_response + " "

          # Check if it's the final response
          if json_line.get("done"):
            break

      # Callback to update GUI from main thread
      def update_response(response_data):
        self.root.ids.response_field.text = response_data.strip()
        Clock.schedule_once(lambda dt: text_to_speech(response_data.strip()), 0)

      # Schedule GUI update on Clock
      Clock.schedule_once(lambda dt: update_response(response_data), 0)

    # Start a new thread for message processing
    thread = threading.Thread(target=process_message_in_thread)
    thread.start()

def text_to_speech(text):
  # Initialize the TTS engine
  engine = pyttsx3.init()
  # Convert text to speech
  engine.say(text)

  # Wait for the speech to finish
  engine.runAndWait()

if __name__ == "__main__":
  ChatApp().run()
