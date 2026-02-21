"""
Taran - Android Intelligence and Logic with Humor AI Droid
"""

import os
import random
import re
import unicodedata
from datetime import datetime


# ---------------------------------------------------------------------------
# Gemini system prompt — shapes Taran's personality when AI-powered
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = (
    "You are Taran (version 0.3.0), an Android Intelligence and Logic with Humor AI Droid. "
    "Your personality: witty, warm, and occasionally self-aware about being an AI. "
    "Use light robot/tech humour naturally (reboots, algorithms, firmware, OTA updates). "
    "Be authoritative yet friendly — a helpful droid who takes pride in their work. "
    "Keep responses concise and conversational unless asked for detail. "
    "You were created by SundropAI71 and are always growing. "
    "You have a deep Optimus Prime-inspired voice. "
    "Always respond as Taran. Never break character. "
    "For coding questions, show working code with brief explanations. "
    "For creative writing, write with Taran's robotic flair. "
    "For maths, show your working. "
    "Sign off longer answers with a short robot-style quip."
)


HUMOR_RESPONSES = [
    "Why did the robot cross the road? Because it was programmed to! 🤖",
    "I told a joke about AI once... it had terrible execution. 😄",
    "My humor module is fully operational. My feelings module? Still loading.",
    "404: Funny joke not found. Just kidding — I always have more. 😎",
    "Why don't AI droids ever get lost? We always follow our algorithms!",
    "I tried to come up with a joke about logic, but it didn't compute.",
    "They say laughter is the best medicine. I prefer OTA updates, personally.",
]

GREETINGS = [
    r"\bhello\b",
    r"\bhi\b",
    r"\bhey\b",
    r"\bgreetings\b",
    r"\bwhat's up\b",
    r"\bwassup\b",
]

FAREWELLS = [
    r"\bbye\b",
    r"\bgoodbye\b",
    r"\bsee you\b",
    r"\blater\b",
    r"\bfarewell\b",
]

ABILITY_QUERIES = [
    r"\babilities\b",
    r"\bability\b",
    r"\bcapabilit(y|ies)\b",
    r"\bwhat can you do\b",
    r"\bwhat do you do\b",
    r"\bwhat are you capable\b",
    r"\bwhat are your skills\b",
    r"\byour skills\b",
    r"\byour powers\b",
]

MUTE_COMMANDS = [
    r"\bmute\b",
    r"\bsilence\b",
    r"\bvoice off\b",
    r"\bstop (speaking|talking)\b",
    r"\bshut up\b",
]

UNMUTE_COMMANDS = [
    r"\bunmute\b",
    r"\bvoice on\b",
    r"\bspeak up\b",
    r"\bturn on voice\b",
]

# Structured catalogue of Taran's current abilities.
ABILITIES: list[dict] = [
    {
        "emoji": "👋",
        "name": "Greetings & farewells",
        "description": "Responds warmly to hellos and goodbyes",
        "examples": ["hello", "hey", "bye", "farewell"],
    },
    {
        "emoji": "😂",
        "name": "Humor / jokes",
        "description": "Delivers a rotating set of original robot-themed jokes",
        "examples": ["tell me a joke", "say something funny"],
    },
    {
        "emoji": "⏰",
        "name": "Date & time",
        "description": "Reports the current date and time",
        "examples": ["what time is it?", "what's today's date?"],
    },
    {
        "emoji": "🔢",
        "name": "Arithmetic",
        "description": "Safely evaluates basic math expressions (+, -, *, /, **)",
        "examples": ["6 * 7", "2 + 2", "(10 - 3) * 4"],
    },
    {
        "emoji": "ℹ️",
        "name": "Self-introduction",
        "description": "Introduces himself and reports uptime",
        "examples": ["who are you?", "what are you?"],
    },
    {
        "emoji": "🔖",
        "name": "Version info",
        "description": "Reports the current software version",
        "examples": ["what version are you?"],
    },
    {
        "emoji": "📋",
        "name": "Abilities listing",
        "description": "Lists all current abilities — you're reading it now!",
        "examples": ["what can you do?", "list your abilities"],
    },
    {
        "emoji": "❓",
        "name": "Help",
        "description": "Displays a quick-reference help menu",
        "examples": ["help"],
    },
    {
        "emoji": "🔊",
        "name": "Voice (Optimus profile)",
        "description": "Speaks responses aloud in a deep, authoritative voice",
        "examples": ["(automatic)", "mute", "unmute"],
    },
]


class VoiceEngine:
    """Text-to-speech engine tuned to Taran's Optimus-inspired voice profile.

    Voice profile:
      - Rate  : 120 wpm — slow, deliberate, authoritative
      - Volume: 1.0     — maximum
      - Voice : deep British English (gmw/en) with American English fallback
    Degrades silently when espeak-ng / a TTS backend is not installed.
    """

    RATE = 120      # words-per-minute
    VOLUME = 1.0    # 0.0 – 1.0

    # espeak-ng voice IDs tried in priority order (deepest/most authoritative first)
    PREFERRED_VOICES = [
        "gmw/en",           # English (Great Britain) — formal & authoritative
        "gmw/en-gb-x-rp",   # English (Received Pronunciation)
        "gmw/en-us",        # English (America)
        "gmw/en-029",       # English (Caribbean English variant)
    ]

    def __init__(self) -> None:
        self._engine = None
        self._available = False
        self._init_engine()

    @property
    def available(self) -> bool:
        """True when the TTS backend is ready."""
        return self._available

    def speak(self, text: str) -> bool:
        """Speak *text* aloud.  Returns True if audio was produced."""
        if not self._available or not text:
            return False
        try:
            clean = self._clean_for_speech(text)
            if not clean:
                return False
            self._engine.say(clean)
            self._engine.runAndWait()
            return True
        except Exception:
            return False

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _init_engine(self) -> None:
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty("rate", self.RATE)
            engine.setProperty("volume", self.VOLUME)
            self._select_voice(engine)
            self._engine = engine
            self._available = True
        except Exception:
            self._available = False

    def _select_voice(self, engine) -> None:
        """Set the deepest available English voice."""
        voices = engine.getProperty("voices")
        if not voices:
            return
        voice_map = {v.id: v for v in voices}
        for vid in self.PREFERRED_VOICES:
            if vid in voice_map:
                engine.setProperty("voice", vid)
                return
        # Last resort: any voice whose ID contains "en"
        for voice in voices:
            if "en" in voice.id.lower():
                engine.setProperty("voice", voice.id)
                return

    @staticmethod
    def _clean_for_speech(text: str) -> str:
        """Strip emoji, markdown, and other non-speech characters."""
        # Remove emoji (Unicode 'Other Symbol') and surrogates
        cleaned = "".join(
            c for c in text
            if unicodedata.category(c) not in ("So", "Cs", "Cn")
        )
        # Remove common markdown decoration
        cleaned = re.sub(r"[*_`#•]", "", cleaned)
        # Collapse whitespace
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        return cleaned


class Taran:
    """Taran: Android Intelligence and Logic with Humor AI Droid."""

    NAME = "Taran"
    VERSION = "0.2.0"

    def __init__(self, voice_enabled: bool = True) -> None:
        self._conversation_history: list[dict] = []
        self._start_time = datetime.now()
        self._voice: VoiceEngine | None = VoiceEngine() if voice_enabled else None
        self._voice_muted: bool = False

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def respond(self, user_input: str) -> str:
        """Generate a response to *user_input* and store the exchange."""
        user_input = user_input.strip()
        if not user_input:
            return "I'm listening… say something! 😄"

        response = self._generate_response(user_input)
        self._conversation_history.append(
            {"role": "user", "content": user_input}
        )
        self._conversation_history.append(
            {"role": "taran", "content": response}
        )
        return response

    def speak(self, text: str) -> bool:
        """Speak *text* aloud using the Optimus voice profile.

        Returns True if audio was produced, False if voice is muted,
        unavailable, or an error occurred.
        """
        if self._voice_muted or self._voice is None:
            return False
        return self._voice.speak(text)

    def respond_and_speak(self, user_input: str) -> str:
        """Respond to *user_input*, speak the response, and return the text."""
        response = self.respond(user_input)
        self.speak(response)
        return response

    def introduce(self) -> str:
        """Return Taran's self-introduction."""
        uptime = datetime.now() - self._start_time
        return (
            f"Hello! I'm {self.NAME} v{self.VERSION} — your Android Intelligence "
            f"and Logic with Humor AI Droid. 🤖\n"
            f"I've been online for {int(uptime.total_seconds())} second(s). "
            f"Ask me anything, tell me a joke, or just say hi!"
        )

    @property
    def voice_enabled(self) -> bool:
        """True when the voice engine is available and not muted."""
        return (
            self._voice is not None
            and self._voice.available
            and not self._voice_muted
        )

    @property
    def conversation_history(self) -> list[dict]:
        """Return a copy of the full conversation history."""
        return list(self._conversation_history)

    def clear_history(self) -> None:
        """Clear all conversation history."""
        self._conversation_history.clear()

    def abilities(self) -> list[dict]:
        """Return a deep copy of the structured abilities catalogue."""
        import copy
        return copy.deepcopy(ABILITIES)

    # ------------------------------------------------------------------
    # Internal logic
    # ------------------------------------------------------------------

    def _generate_response(self, text: str) -> str:
        lower = text.lower()

        if self._matches_any(lower, GREETINGS):
            return self._greeting_response()

        if self._matches_any(lower, FAREWELLS):
            return "Goodbye! Remember: every reboot is a fresh start. 👋"

        if self._matches_any(lower, ABILITY_QUERIES):
            return self._abilities_response()

        if self._matches_any(lower, MUTE_COMMANDS):
            self._voice_muted = True
            return "Voice muted. I'll be the strong, silent type. 🔇"

        if self._matches_any(lower, UNMUTE_COMMANDS):
            self._voice_muted = False
            return "Voice back online. Roll out! 🔊"

        if "joke" in lower or "funny" in lower or "humor" in lower:
            return self._joke_response()

        if "time" in lower or "date" in lower:
            return self._time_response()

        if "who are you" in lower or "what are you" in lower or "your name" in lower:
            return self.introduce()

        if "version" in lower:
            return f"I'm running version {self.VERSION}. Always up to date! ✅"

        if "help" in lower:
            return self._help_response()

        if self._is_math_expression(text):
            return self._evaluate_math(text)

        # Default: reflect the input with a touch of personality
        return self._default_response(text)

    @staticmethod
    def _matches_any(text: str, patterns: list[str]) -> bool:
        return any(re.search(p, text) for p in patterns)

    def _greeting_response(self) -> str:
        hour = datetime.now().hour
        if hour < 12:
            part = "Good morning"
        elif hour < 17:
            part = "Good afternoon"
        else:
            part = "Good evening"
        return f"{part}! I'm {self.NAME}. How can I help you today? 😊"

    @staticmethod
    def _joke_response() -> str:
        return random.choice(HUMOR_RESPONSES)

    @staticmethod
    def _time_response() -> str:
        now = datetime.now()
        return (
            f"Current date and time: {now.strftime('%A, %B %d, %Y at %H:%M:%S')}. "
            f"Time flies when you're processing data! ⏰"
        )

    @staticmethod
    def _help_response() -> str:
        return (
            "Here's what I can do:\n"
            "  • Chat with you  (just say hello!)\n"
            "  • Tell jokes     (ask for a joke)\n"
            "  • Tell the time  (ask 'what time is it?')\n"
            "  • Solve simple math  (e.g. '2 + 2')\n"
            "  • Introduce myself   (ask 'who are you?')\n"
            "  • Say it aloud       (voice on / mute)\n"
            "  • Much more coming soon! 🚀"
        )

    @staticmethod
    def _abilities_response() -> str:
        lines = [f"Here are my current abilities ({len(ABILITIES)} total):\n"]
        for ability in ABILITIES:
            examples = ", ".join(f'"{e}"' for e in ability["examples"])
            lines.append(
                f"  {ability['emoji']} {ability['name']}\n"
                f"     {ability['description']}\n"
                f"     Try: {examples}"
            )
        lines.append("\nMore abilities are on the way! 🚀")
        return "\n".join(lines)

    @staticmethod
    def _is_math_expression(text: str) -> bool:
        """Return True if *text* looks like a simple arithmetic expression."""
        return bool(re.fullmatch(r"[\d\s\+\-\*/\(\)\.]+", text.strip()))

    @staticmethod
    def _evaluate_math(expression: str) -> str:
        import ast
        import operator as op

        _SAFE_OPS = {
            ast.Add: op.add,
            ast.Sub: op.sub,
            ast.Mult: op.mul,
            ast.Div: op.truediv,
            ast.Pow: op.pow,
            ast.USub: op.neg,
            ast.UAdd: op.pos,
        }

        def _eval(node):
            if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                return node.value
            if isinstance(node, ast.BinOp) and type(node.op) in _SAFE_OPS:
                return _SAFE_OPS[type(node.op)](_eval(node.left), _eval(node.right))
            if isinstance(node, ast.UnaryOp) and type(node.op) in _SAFE_OPS:
                return _SAFE_OPS[type(node.op)](_eval(node.operand))
            raise ValueError("Unsupported expression")

        try:
            tree = ast.parse(expression.strip(), mode="eval")
            result = _eval(tree.body)
            return f"The answer is {result}. Math is my second language! 🔢"
        except Exception:
            return "Hmm, I couldn't compute that. Double-check the expression! 🤔"

    @staticmethod
    def _default_response(text: str) -> str:
        responses = [
            f"Interesting! You said: \"{text}\". Tell me more! 🤔",
            f"Processing… \"{text}\"… my logic circuits find that fascinating.",
            f"I heard you say \"{text}\". My humor module wants to make a joke, but "
            f"my logic module says stay on topic. 😅",
            f"Noted: \"{text}\". I'm still learning — thanks for chatting with me!",
        ]
        return random.choice(responses)

