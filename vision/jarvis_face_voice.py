import os
import time
import cv2
import speech_recognition as sr
import pyttsx3
import requests

# Face recognition pipeline using Haar cascades
CASCADE_PATH = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
FACE_CASCADE = cv2.CascadeClassifier(CASCADE_PATH)


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening for command...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "I couldn't understand that."
    except sr.RequestError:
        return "The speech service is unavailable."


def get_reply(message):
    text = message.lower().strip()
    if not text:
        return "I heard nothing."
    if any(word in text for word in ["hello", "hi", "hey"]):
        return "Hello! I am Jarvis and I can see you."
    if "time" in text:
        from datetime import datetime
        return f"The current time is {datetime.now().strftime('%I:%M %p')}."
    if "date" in text:
        from datetime import datetime
        return f"Today is {datetime.now().strftime('%A, %B %d, %Y')}."
    if "weather" in text:
        try:
            response = requests.get('https://wttr.in/New%20York?format=3', timeout=5)
            if response.ok:
                return f"Weather: {response.text.strip()}"
        except Exception:
            pass
        return "I can check the weather for you."
    if "who are you" in text or "your name" in text:
        return "I am Jarvis, your AI assistant with voice and face recognition."
    if "exit" in text or "stop" in text:
        return "Goodbye."
    return "I heard you. Please tell me what you want me to do."


def start_camera_session():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Camera not available.")
        return

    speak("Jarvis vision system online. I am ready.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to read frame.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = FACE_CASCADE.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "Face Detected", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow('Jarvis Vision', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

        if len(faces) > 0:
            command = listen_for_command()
            reply = get_reply(command)
            print(reply)
            speak(reply)
            if "goodbye" in reply.lower() or "exit" in command.lower():
                break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    start_camera_session()
