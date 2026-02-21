"""
Entry point for Taran — Android Intelligence and Logic with Humor AI Droid.

Run:
    python main.py
"""

from taran import Taran


def main() -> None:
    taran = Taran(voice_enabled=True)
    print(taran.introduce())

    if taran.voice_enabled:
        print("🔊 Optimus voice profile active — Taran will speak his responses.")
    else:
        print("🔇 Voice unavailable (espeak-ng not installed?). Text-only mode.")

    print("\nType 'quit' or 'exit' to stop.  Say 'mute' / 'unmute' to toggle voice.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nTaran: Shutting down. Stay logical! 👋")
            break

        if user_input.lower() in {"quit", "exit"}:
            print("Taran: Goodbye! See you next boot cycle. 🤖")
            break

        if not user_input:
            continue

        response = taran.respond_and_speak(user_input)
        print(f"Taran: {response}\n")


if __name__ == "__main__":
    main()
