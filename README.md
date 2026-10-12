# Jarvis Assistant

A multi-version Jarvis-style assistant project with:

- Web version in HTML/JavaScript
- Desktop app version in Python/Tkinter
- AI-powered assistant with OpenAI integration
- Voice + face recognition version using webcam + speech

## Project structure

- `web/` — browser-based assistant
- `desktop/` — desktop GUI app
- `ai/` — Flask API + AI backend
- `vision/` — webcam face + voice assistant
- `requirements.txt` — Python dependencies

## Quick start

### 1) Install Python dependencies

```bash
pip install -r requirements.txt
```

### 2) Start the AI backend (optional but recommended)

```bash
python ai/jarvis_ai.py
```

The server runs on:

- http://localhost:8000/health
- http://localhost:8000/chat

Set an environment variable to enable OpenAI mode:

```bash
export OPENAI_API_KEY=your_key_here
```

On Windows PowerShell:

```powershell
$env:OPENAI_API_KEY="your_key_here"
```

### 3) Run the web app

Open `web/index.html` in a browser, or serve the folder:

```bash
cd web
python -m http.server 8080
```

Then open http://localhost:8080

### 4) Run the desktop app

```bash
python desktop/jarvis_desktop.py
```

### 5) Run the face + voice version

```bash
python vision/jarvis_face_voice.py
```

This version uses your webcam and microphone.

## Features

- Voice command recognition
- Text chat responses
- Time/date lookup
- Weather lookup (via wttr.in)
- OpenAI-powered responses when API key is configured
- Face detection using OpenCV
- Browser UI and desktop app variants

## Notes

- The web interface works with the backend if running.
- Speech features depend on microphone access.
- Face detection requires a webcam and camera drivers.

## License

MIT
