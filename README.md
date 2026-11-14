# JARVIS — Python Voice Assistant + Web Edition

This repository preserves the original Tkinter desktop assistant in `jarvis.py` and adds a browser-based version powered by FastAPI.

## Web edition features

- Chat-style browser interface
- Text commands
- Optional microphone input using browser Speech Recognition (where supported)
- Spoken replies using browser speech synthesis
- Time/date, Wikipedia summaries, and Google/YouTube shortcuts
- Health endpoint at `/health`

The public web version cannot control your Windows desktop, access local files, or send email. Those features remain outside this hosted demo for security and architecture reasons.

## Run locally (Windows)

1. Install Python 3.10 or newer.
2. Open a terminal in this repository.
3. Create and activate a virtual environment:

```powershell
py -m venv .venv
.venv\Scripts\activate
```

4. Install dependencies:

```powershell
pip install -r requirements.txt
```

5. Start the server:

```powershell
uvicorn app:app --reload
```

6. Open http://127.0.0.1:8000 in Chrome or Edge.

## Deploy on Render

Create a **Web Service** connected to this repository:

- Runtime: Python 3
- Branch: `main`
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn app:app --host 0.0.0.0 --port $PORT`

No API key is required for this initial version. After deployment, test `/health` and the home page. Render's free web services may sleep after inactivity, so the first request after a quiet period can take longer.

## Project files

- `jarvis.py` — original desktop/Tkinter implementation
- `app.py` — FastAPI web application
- `requirements.txt` — web dependencies
