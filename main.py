import argparse
import os
import time
import pyttsx3
import speech_recognition as sr
import openai

LANGUAGES = {
    "en-US": "English (US)",
    "en-GB": "English (UK)",
    "zh-CN": "Chinese (Simplified)",
    "es-ES": "Spanish",
    "fr-FR": "French",
    "de-DE": "German",
    "it-IT": "Italian",
    "ja-JP": "Japanese",
    "ko-KR": "Korean",
    "pt-BR": "Portuguese (Brazil)",
    "ru-RU": "Russian",
}

def transcribe_speech(language):
    # set up the speech recognizer
    r = sr.Recognizer()
    transcribed_text = ""
    while True:
        try:
            # listen for speech with a timeout of 5 seconds
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source, timeout=5)
            # transcribe the audio to text
            transcribed_speech = r.recognize_google(audio, language=language)
            print(f"You said: {transcribed_speech}")
            # concatenate the transcribed text into a single paragraph
            transcribed_text += transcribed_speech + ". " # type: ignore
        except sr.WaitTimeoutError:
            print("No speech detected. Please speak again.")
            continue
        except sr.UnknownValueError:
            print("Could not understand audio")
            continue
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            continue
        if input("Press Enter to stop recording, or press any other keys to keep recording: ") == "":
            break

    return transcribed_text

def send_request(language: str, words: str) -> None:
    
    """
        Sends a request to the OpenAI API and speaks out the response.

        Args:
            language: A string indicating the language code of the chat message.
            words: A string containing the chat message to be sent.

        Returns:
            None.

        Raises:
            openai.error.OpenAIError: If there is an error with the OpenAI API request.
    """
    
    # Get the API key from the environment variable in Windows
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    # Send the chat message to the OpenAI API 
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo-0301",
      messages=[
        {
            "role": "user", 
            "content": words
        }
      ]
    )
    
    # Get the response from the OpenAI API
    answer = completion.choices[0].message["content"] # type: ignore
    # Print the response
    print("OpenAI API response:")
    print(answer)

    # Speak out the response
    # Add try-except block to handle exceptions
    try:
        speak(answer, language)
    except Exception as e:
        print(e)
        print("Could not speak out the response. Please try again.")
        return

    # return

def speak(text: str, language: str) -> None:
    """
    Speaks the given text using the appropriate voice for the given language.

    Args:
        text: A string containing the text to speak.
        language: A string indicating the language code of the text. 
                  This has to be converted to language name.

    Returns:
        None.
    """
    # Initialize the pyttsx engine
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 1.0)

    # Set the voice for the given language
    engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_11.0')

    # Convert language code to pyttsx language name, using the LANGUAGES dictionary
    language = LANGUAGES.get(language, "english").split()[0].lower()
    print(f"Speaking out the response in {language}...")

    if language == 'chinese':
        # Use the Tingting voice for Chinese
        voices = engine.getProperty('voices')
        for voice in voices:
            if 'tingting' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break

    engine.say(text)
    engine.runAndWait()
    engine.stop()
    

if __name__ == "__main__":
    # check for arguments
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    if len(args.__dict__) > 0:
        parser.print_usage()
        exit(1)

    # prompt user to select language
    print("Supported languages:")
    for i, (code, name) in enumerate(LANGUAGES.items(), start=1):
        print(f"{i}. {name}")
    while True:
        language = input("Select a language by number (default: 1): ")
        if not language:
            language = "1"
        elif not language.isdigit() or int(language) not in range(1, len(LANGUAGES) + 1):
            print("Invalid language selected. Please try again.")
            continue
        else:
            language = int(language)
            break

    # convert language number to language code
    language_code = list(LANGUAGES.keys())[language - 1]

    # loop indefinitely
    while True:
        # transcribe speech from the microphone
        words = transcribe_speech(language_code)

        # send the chat message to the OpenAI API
        if words:
            print("Sending request to OpenAI API...")
            send_request(language_code, words)
        else:
            print("No speech detected. Please speak again.")

        # prompt the user to press enter to continue, and Q to quit
        if input("Press Q to quit, or press any other keys to continue: ").lower() == "q":
            break


        # pause for 1 second before continuing
        time.sleep(1)