import requests
import json
import pyttsx3

def send_message(message):
    # Define the endpoint URL
    url = "http://localhost:11434/api/generate"

    # Define the payload (data) to be sent in the request
    data = {
        "model": "llama2",
        "prompt": message,
        "stream": False
    }

    # Send the POST request to the API endpoint
    response = requests.post(url, json=data)

    # Check for HTTP errors
    response.raise_for_status()

    # Parse the JSON response
    response_data = response.json()

    # Extract the assistant's response
    if 'response' in response_data:
        assistant_response = response_data['response']
    else:
        assistant_response = "Sorry, I couldn't understand the response."

    return assistant_response.strip()

def text_to_speech(text):
    # Initialize the TTS engine
    engine = pyttsx3.init()
    # Convert text to speech
    engine.say(text)
    # Wait for the speech to finish
    engine.runAndWait()

def print_banner():
    sheep = r"""
         __  _
    .-:'  `; `-._
   (_,           )
 ,'o"(            )>
(__,-'            )
   (             )
    `-'._.--._.-'
"""

    print(sheep)

def main():
    print_banner()
    print("Welcome to Ollama Chatbot")
    print("Type 'exit' to end the conversation.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Exiting...")
            break

        # Send user's message to the server and get the assistant's response
        assistant_response = send_message(user_input)

        # Display the assistant's response on the console
        print("\nAssistant:", assistant_response)

        # Convert the assistant's response to speech
        text_to_speech(assistant_response)

if __name__ == "__main__":
    main()
