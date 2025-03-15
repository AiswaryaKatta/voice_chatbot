# voice_utils.py
import speech_recognition as sr
import pyttsx3

# Initialize the recognizer and text-to-speech engine.
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

def speak(text):
    """Convert text to speech and print the output for debugging."""
    print("Speaking:", text)
    tts_engine.say(text)
    tts_engine.runAndWait()

def listen():
    """Listen for audio input and return recognized text."""
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        speak("Sorry, I did not understand that.")
        return None
    except sr.RequestError:
        speak("Sorry, there was an error with the speech recognition service.")
        return None
