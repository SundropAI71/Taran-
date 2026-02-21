# Taran 🤖

> **Android Intelligence and Logic with Humor AI Droid**

Taran is a conversational AI droid built in Python. He can chat, tell jokes, answer questions, solve simple math, and keep you company — all with a healthy sense of humor. And now he speaks in a deep, authoritative Optimus Prime-inspired voice. 🔊

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

### Run Taran

```bash
python main.py
```

### Example session

```
Hello! I'm Taran v0.2.0 — your Android Intelligence and Logic with Humor AI Droid. 🤖
I've been online for 0 second(s). Ask me anything, tell me a joke, or just say hi!
🔊 Optimus voice profile active — Taran will speak his responses.

Type 'quit' or 'exit' to stop.  Say 'mute' / 'unmute' to toggle voice.

You: hello
Taran: Good morning! I'm Taran. How can I help you today? 😊

You: tell me a joke
Taran: Why did the robot cross the road? Because it was programmed to! 🤖

You: 6 * 7
Taran: The answer is 42. Math is my second language! 🔢

You: mute
Taran: Voice muted. I'll be the strong, silent type. 🔇

You: unmute
Taran: Voice back online. Roll out! 🔊

You: bye
Taran: Goodbye! See you next boot cycle. 🤖
```

---

## Voice Profile — Optimus

Taran's voice is tuned to sound deep and authoritative:

| Setting | Value | Effect |
|---|---|---|
| Engine | espeak-ng (`gmw/en`) | Deep British English |
| Rate | 120 wpm | Slow and deliberate |
| Volume | 1.0 | Maximum |

**Voice commands**

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
├── taran.py          # Core Taran AI class + VoiceEngine
├── main.py           # Interactive CLI entry point
├── requirements.txt  # Python dependencies
└── tests/
    └── test_taran.py # Unit tests (71 tests)
```

---

## Roadmap

- [ ] Google Gemini AI integration (full LLM brain)
- [ ] Persistent memory across sessions
- [ ] Plugin system for new skills
- [ ] Android app integration
- [ ] Expanded knowledge base
