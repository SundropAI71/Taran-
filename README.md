# Taran 🤖

> **Android Intelligence and Logic with Humor AI Droid**

Taran is a conversational AI droid built in Python. He can chat, tell jokes, answer questions, solve simple math, and keep you company — all with a healthy sense of humor. And now he speaks in a deep, authoritative Optimus Prime-inspired voice. 🔊

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

## Getting Started

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

Then open **http://localhost:5000** in your browser.

On Android or any device on the same network, open **http://\<your-local-ip\>:5000**.

### Or run in the terminal (CLI)

```bash
python main.py
```

---

## App UI

The web app provides a full chat interface:

- 💬 **Message bubbles** — user messages on the right, Taran on the left
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
├── requirements.txt  # Python dependencies
├── templates/
│   └── index.html    # Chat UI (dark theme, mobile-friendly)
└── tests/
    ├── test_taran.py # Core AI unit tests (71 tests)
    └── test_app.py   # Flask route tests (23 tests)
```

---

## Roadmap

- [ ] Google Gemini AI integration (full LLM brain)
- [ ] Persistent memory across sessions
- [ ] Plugin system for new skills
- [ ] Android native app
- [ ] Expanded knowledge base
