"""
Taran - Android Intelligence and Logic with Humor AI Droid
"""

import random
import re
from datetime import datetime


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
]


class Taran:
    """Taran: Android Intelligence and Logic with Humor AI Droid."""

    NAME = "Taran"
    VERSION = "0.1.0"

    def __init__(self):
        self._conversation_history: list[dict] = []
        self._start_time = datetime.now()

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
