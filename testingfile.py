import speech_recognition as sr
import pyttsx3
engine = pyttsx3.init()
r = sr.Recognizer()
with sr.Microphone(device_index=1) as source:
    audio = r.listen(source)

query = r.recognize_google(audio, language="ru-RU")
print(query.split())
engine.say(query)
engine.runAndWait()