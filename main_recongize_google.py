import argparse
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

def send_request(language, prompt):
    # set up the OpenAI API client
    openai.api_key = openai_secret_manager.get_secret("openai")["api_key"]

    # generate autocompletions for the prompt
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=60,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = response.choices[0].text.strip()
    print(f"Response: {message}")

    # speak the response
    engine = pyttsx3.init()
    engine.say(message)
    engine.runAndWait()

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
            #send_request(language_code, words)
        else:
            print("No speech detected. Please speak again.")

        # prompt the user to press enter to continue
        input("Press Enter to continue...")

        # pause for 1 second before continuing
        time.sleep(1)