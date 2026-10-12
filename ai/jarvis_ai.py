import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("OPENAI_API_KEY")


def fallback_reply(message: str) -> str:
    text = message.lower().strip()

    if not text:
        return "I heard you, but the message was empty."
    if any(word in text for word in ["hello", "hi", "hey"]):
        return "Hello! I am Jarvis. How can I help you today?"
    if "time" in text:
        from datetime import datetime
        return f"The current time is {datetime.now().strftime('%I:%M %p')}."
    if "date" in text:
        from datetime import datetime
        return f"Today is {datetime.now().strftime('%A, %B %d, %Y')}."
    if "weather" in text:
        city = "New York"
        if "in " in text:
            parts = text.split("in ", 1)
            if len(parts) > 1:
                city = parts[1].strip().title()
        try:
            response = requests.get(f"https://wttr.in/{city}?format=3", timeout=5)
            if response.status_code == 200:
                return f"Weather in {city}: {response.text.strip()}"
        except Exception:
            pass
        return f"I can check the weather for {city} if you want."
    if "who are you" in text or "your name" in text:
        return "I am Jarvis, your personal assistant."
    if "thank" in text:
        return "You are welcome."
    return "I heard you. Please tell me what you want me to do."


def get_openai_reply(message: str) -> str:
    if not API_KEY:
        return fallback_reply(message)

    try:
        from openai import OpenAI
        client = OpenAI(api_key=API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are Jarvis, a helpful and concise AI assistant."},
                {"role": "user", "content": message},
            ],
            temperature=0.7,
            max_tokens=250,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return fallback_reply(message)


@app.get("/health")
def health():
    return {"status": "ok", "mode": "openai" if API_KEY else "local"}


@app.post("/chat")
def chat():
    payload = request.get_json(silent=True) or {}
    message = str(payload.get("message", "")).strip()
    if not message:
        return jsonify({"reply": "I didn't receive any message."})

    reply = get_openai_reply(message)
    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
