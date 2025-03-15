import speech_recognition as sr

recognizer = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = recognizer.listen(source)
try:
    text = recognizer.recognize_google(audio)
    print("You said:", text)
except Exception as e:
    print("Error:", e)
