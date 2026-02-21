# Taran 🤖

> **Android Intelligence and Logic with Humor AI Droid**

Taran is a conversational AI droid built in Python. He can chat, tell jokes, answer questions, solve simple math, and keep you company — all with a healthy sense of humor.

---

## Features

| Capability | Example input |
|---|---|
| 👋 Greetings & farewells | `hello`, `bye` |
| 😂 Humor / jokes | `tell me a joke` |
| ⏰ Date & time | `what time is it?` |
| 🔢 Arithmetic | `6 * 7` |
| ℹ️ Self-introduction | `who are you?` |
| ❓ Help | `help` |

---

## Getting Started

### Requirements
- Python 3.9+

### Run Taran

```bash
python main.py
```

### Example session

```
Hello! I'm Taran v0.1.0 — your Android Intelligence and Logic with Humor AI Droid. 🤖
I've been online for 0 second(s). Ask me anything, tell me a joke, or just say hi!

Type 'quit' or 'exit' to stop.

You: hello
Taran: Good morning! I'm Taran. How can I help you today? 😊

You: tell me a joke
Taran: Why did the robot cross the road? Because it was programmed to! 🤖

You: 6 * 7
Taran: The answer is 42. Math is my second language! 🔢

You: bye
Taran: Goodbye! See you next boot cycle. 🤖
```

---

## Running Tests

```bash
python -m pytest tests/ -v
```

---

## Project Structure

```
Taran-/
├── taran.py          # Core Taran AI class
├── main.py           # Interactive CLI entry point
├── requirements.txt  # Python dependencies
└── tests/
    └── test_taran.py # Unit tests
```

---

## Roadmap

- [ ] Persistent memory across sessions
- [ ] Plugin system for new skills
- [ ] Voice interface
- [ ] Android app integration
- [ ] Expanded knowledge base
