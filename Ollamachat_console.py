import re
import requests
import json
import pyttsx3

def send_message(message, model, real_time_output_enabled=True):
    # Define the endpoint URL
    url = "http://localhost:11434/api/chat"

    # Define the payload (data) to be sent in the request
    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": message}
        ]
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
            assistant_response = json_line['message']['content']
            
            # Ensure the assistant's response is properly formatted
            assistant_response = assistant_response.strip()

            response_data += assistant_response + " "

            # Check if it's the final response
            if json_line.get("done"):
                break

            # Add assistant's response to the buffer
            sentence_buffer.append(assistant_response)

            # Check if the assistant's response ends with punctuation indicating the end of a sentence
            if assistant_response.endswith(('.', '!', '?')):
                # Print the buffered responses if real-time output is enabled
                if real_time_output_enabled:
                    print("\nAssistant:", ' '.join(sentence_buffer))
                sentence_buffer = []

    return response_data.strip()


def text_to_speech(text):
    # Initialize the TTS engine
    engine = pyttsx3.init()
    # Convert text to speech
    engine.say(text)

    # Wait for the speech to finish
    engine.runAndWait()


def main():
    print("Ollama Chatbot")
    print("Type 'exit' to end the conversation.")
    print("Make sure you already installed those models.")
    # Prompt user to select a model
    print("Models that you may have installed:")
    print("1. llama2-uncensored")
    print("2. llama3")
    print("3. phi3")
    print("4. wizardlm2")
    print("5. mistral")
    print("6. gemma")
    print("7. mixtral")
    print("8. llama2")
    print("9. Custom Model")
    model_choice = input("Please select a model (enter the number), or press Enter for 'llama3': ")

    models = {
        '1': 'llama2-uncensored',
        '2': 'llama3',
        '3': 'phi3',
        '4': 'wizardlm2',
        '5': 'mistral',
        '6': 'gemma',
        '7': 'mixtral',
        '8': 'llama2'
    }

    selected_model = models.get(model_choice)
    if not selected_model:
        if model_choice == '':
            selected_model = 'llama3'  # Default to llama3 if user presses Enter
        elif model_choice == '9':
            selected_model = input("Enter the name of the custom model: ")
        else:
            print("Invalid model choice. Exiting...")
            return

    text_to_speech_option = input("Do you want to enable text-to-speech? (y/n), or press Enter to turn off: ")
    if text_to_speech_option.lower() == 'y':
        text_to_speech_enabled = True
    elif text_to_speech_option == '':
        text_to_speech_enabled = False  # Turn off text-to-speech if user presses Enter
    else:
        print("Invalid input. Text-to-speech disabled.")
        text_to_speech_enabled = False
    
    real_time_output_option = input("Do you want to see real-time output? (y/n), or press Enter for yes: ")
    if real_time_output_option.lower() == 'n':
        real_time_output_enabled = False
    elif real_time_output_option == '':
        real_time_output_enabled = True
    else:
        print("Invalid input. Real-time output enabled.")
        real_time_output_enabled = True

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Exiting...")
            break

        # Send user's message to the server with the selected model
        assistant_response = send_message(user_input, selected_model, real_time_output_enabled)

        # Display the assistant's response on the console
        print("\nAssistant:", assistant_response)

        # Convert the assistant's response to speech if enabled
        if text_to_speech_enabled:
            text_to_speech(assistant_response)

if __name__ == "__main__":
    main()
