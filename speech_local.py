# speech_local.py
import speech_recognition as sr
import pyttsx3
from assistant_core import Assistant

def listen_and_respond():
    assistant = Assistant()
    r = sr.Recognizer()
    mic = sr.Microphone()
    engine = pyttsx3.init()
    print("Say something (ctrl-c to quit)...")
    with mic as source:
        r.adjust_for_ambient_noise(source)
        while True:
            print("Listening...")
            audio = r.listen(source, timeout=None, phrase_time_limit=6)
            try:
                text = r.recognize_google(audio)
                print("You said:", text)
                res = assistant.handle(text)
                print("Assistant:", res["text"])
                engine.say(res["text"])
                engine.runAndWait()
            except sr.UnknownValueError:
                print("Sorry, I didn't understand.")
            except sr.RequestError as e:
                print(f"Speech recognition service error: {e}")

if __name__ == "__main__":
    listen_and_respond()
