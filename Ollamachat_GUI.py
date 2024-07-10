import threading
from kivy.clock import Clock
from kivy.lang import Builder
from kivymd.app import MDApp
import requests
import json
#import pyttsx3

# Load KivyMD design string
kv_string = '''
BoxLayout:
  orientation: 'vertical'
  padding: dp(20)

  ScrollView:
    BoxLayout:
      orientation: 'vertical'
      size_hint_y: None
      height: self.minimum_height

      BoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        height: self.minimum_height
        spacing: dp(10)

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
        multiline: True  # Allow multiline for longer responses
        size_hint_y: None
        height: self.minimum_height  # Ensure it grows to fit content
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
      url = "http://localhost:11434/api/generate"

      # Define the payload (data) to be sent in the request
      data = {
        "model": "llama2",
        "prompt": user_input,
        "stream": False
      }

      # Send the POST request to the API endpoint
      response = requests.post(url, json=data)

      # Parse the JSON response
      response_data = response.json()

      print(response)

      # Extract the assistant's response
      if 'response' in response_data:
        assistant_response = response_data['response']
      else:
        assistant_response = "Sorry, I couldn't understand the response."

      # Callback to update GUI from main thread
      def update_response(response_data):
        self.root.ids.response_field.text = response_data

      # Schedule GUI update on Clock
      Clock.schedule_once(lambda dt: update_response(assistant_response), 0)

    # Start a new thread for message processing
    thread = threading.Thread(target=process_message_in_thread)
    thread.start()

if __name__ == "__main__":
  ChatApp().run()
