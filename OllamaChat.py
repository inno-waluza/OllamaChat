import requests
import json
import pyttsx3

def send_message(message):
    # Define the endpoint URL
    url = "http://localhost:11434/api/chat"

    # Define the payload (data) to be sent in the request
    data = {
        "model": "llama2-uncensored",
        "messages": [
            {"role": "user", "content": message}
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

    return response_data.strip()

def text_to_speech(text):
    # Initialize the TTS engine
    engine = pyttsx3.init()
    # Convert text to speech
    engine.say(text)

    # Wait for the speech to finish
    engine.runAndWait()

def get_female_voice(engine):
    # Get all available voices
    voices = engine.getProperty('voices')

    # Select a female voice
    female_voice = None
    for voice in voices:
        if "female" in voice.name.lower():
            female_voice = voice
            break

    return female_voice

def main():
    print("Ollama Chatbot")
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
