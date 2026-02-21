# Taran 🤖

> **Android Intelligence and Logic with Humor AI Droid**

Taran is a conversational AI droid built in Python. He can chat, tell jokes, answer questions, solve simple math, and keep you company — all with a healthy sense of humor. And now he speaks in a deep, authoritative Optimus Prime-inspired voice. 🔊

---

## How to Access Taran

### Option A — On your computer (fastest)

```
1. pip install -r requirements.txt
2. python app.py
3. Open  →  http://localhost:5000
```

### Option B — On Android / any phone (same Wi-Fi)

```
1. Run  python app.py  on your computer
2. Look for the URL printed in the terminal, e.g.:
       📱  http://192.168.1.42:5000
3. Type that URL into your phone's browser
   — OR —
   Scan the QR code that appears in the terminal 📷
4. Click 📱 in the app header any time to see the URL + QR again
```

### Option C — From anywhere in the world (cloud deploy)

Deploy Taran to [Render.com](https://render.com) for free in one click — no credit card needed:

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/SundropAI71/Taran-)

**Or manually:**

1. Fork this repo on GitHub
2. Go to [render.com](https://render.com) → **New Web Service**
3. Connect your fork — Render auto-detects `render.yaml`
4. Click **Deploy** — Taran is live at `https://taran-xxxx.onrender.com` 🌐

> Railway and Heroku are also supported via the included `Procfile`.

---

## App

Taran runs as a **web app** — launch it and open it in any browser, including on Android/mobile.

![Taran App](https://github.com/user-attachments/assets/e2c7ad22-45a8-4ef4-bedb-56ce3cb55e9e)

---

## Features

| Capability | Example input |
|---|---|
| 👋 Greetings & farewells | `hello`, `bye` |
| 😂 Humor / jokes | `tell me a joke` |
| ⏰ Date & time | `what time is it?` |
| 🔢 Arithmetic | `6 * 7` |
| ℹ️ Self-introduction | `who are you?` |
| 🔖 Version info | `what version are you?` |
| 📋 Abilities listing | `what can you do?` |
| ❓ Help | `help` |
| 🔊 **Voice (Optimus profile)** | automatic · `mute` · `unmute` |

---

## Getting Started (full setup)

### Requirements
- Python 3.9+
- **Voice** (optional): espeak-ng must be installed for TTS
  - **Linux**: `sudo apt-get install espeak-ng`
  - **macOS**: built-in `say` command (pyttsx3 uses it automatically)
  - **Windows**: built-in SAPI5 voices (pyttsx3 uses them automatically)

### Install Python dependencies

```bash
pip install -r requirements.txt
```

### Run as an App 🚀

```bash
python app.py
```

The terminal prints your **exact URLs** (desktop + mobile) and a **scannable QR code** automatically.

### Or run in the terminal (CLI)

```bash
python main.py
```

---

## App UI

The web app provides a full chat interface:

- 💬 **Message bubbles** — user messages on the right, Taran on the left
- 📱 **Access button** — shows your mobile URL and QR code at any time
- 📋 **Abilities button** — lists all of Taran's current skills
- 🗑️ **Clear button** — wipe the conversation history
- ⌨️ **Enter to send** · **Shift+Enter** for multi-line messages
- 🔄 **Typing indicator** — animated dots while Taran is thinking

### REST API

The app also exposes a simple API for integrations:

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Chat page |
| `POST` | `/chat` | Send `{"message": "..."}`, get `{"response": "..."}` |
| `GET` | `/history` | Full conversation history |
| `POST` | `/clear` | Clear conversation history |
| `GET` | `/abilities` | Taran's abilities catalogue |
| `GET` | `/access` | Returns `local_url`, `mobile_url`, and `qr_ascii` |

---

## Voice Profile — Optimus

Taran's voice is tuned to sound deep and authoritative:

| Setting | Value | Effect |
|---|---|---|
| Engine | espeak-ng (`gmw/en`) | Deep British English |
| Rate | 120 wpm | Slow and deliberate |
| Volume | 1.0 | Maximum |

**Voice commands** (type in the chat):

| Say | Effect |
|---|---|
| `mute` / `silence` / `voice off` | Silence Taran |
| `unmute` / `voice on` / `speak up` | Restore voice |

---

## Running Tests

```bash
python -m pytest tests/ -v
```

---

## Project Structure

```
Taran-/
├── app.py            # Flask web app (chat UI + REST API)
├── taran.py          # Core Taran AI class + VoiceEngine
├── main.py           # Interactive CLI entry point
├── Procfile          # Cloud deploy start command (Railway / Heroku / Render)
├── render.yaml       # Zero-config Render.com deployment
├── runtime.txt       # Python version pin for cloud platforms
├── requirements.txt  # Python dependencies
├── templates/
│   └── index.html    # Chat UI (dark theme, mobile-friendly, QR access panel)
└── tests/
    ├── test_taran.py # Core AI unit tests (71 tests)
    └── test_app.py   # Flask route tests (38 tests)
```

---

## Roadmap

- [ ] Google Gemini AI integration (full LLM brain)
- [ ] Persistent memory across sessions
- [ ] Plugin system for new skills
- [ ] Android native app
- [ ] Expanded knowledge base
