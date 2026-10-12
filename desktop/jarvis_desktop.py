import os
import speech_recognition as sr
import pyttsx3
import requests
from datetime import datetime


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def get_local_reply(message):
    text = message.lower().strip()
    if not text:
        return "I heard nothing. Please say a command."
    if any(word in text for word in ["hello", "hi", "hey"]):
        return "Hello! I am Jarvis. How may I assist you?"
    if "time" in text:
        return f"The current time is {datetime.now().strftime('%I:%M %p')}."
    if "date" in text:
        return f"Today is {datetime.now().strftime('%A, %B %d, %Y')}."
    if "weather" in text:
        city = "New York"
        if "in " in text:
            city = text.split("in ", 1)[1].strip().title()
        try:
            response = requests.get(f"https://wttr.in/{city}?format=3", timeout=5)
            if response.ok:
                return f"Weather in {city}: {response.text.strip()}"
        except Exception:
            pass
        return f"I can check the weather for {city}."
    if "who are you" in text or "your name" in text:
        return "I am Jarvis, your personal assistant."
    if "exit" in text or "stop" in text:
        return "Goodbye."
    return "I heard you. Please tell me what you want me to do."


def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        return "I couldn't understand that."
    except sr.RequestError:
        return "The speech service is unavailable right now."


def main():
    print("Jarvis desktop assistant is running.")
    while True:
        command = listen_for_command()
        reply = get_local_reply(command)
        print(reply)
        speak(reply)
        if "goodbye" in reply.lower() or "exit" in command.lower():
            break


if __name__ == "__main__":
    main()
