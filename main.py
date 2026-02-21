"""
Entry point for Taran — Android Intelligence and Logic with Humor AI Droid.

Run:
    python main.py
"""

from taran import Taran


def main() -> None:
    taran = Taran()
    print(taran.introduce())
    print("\nType 'quit' or 'exit' to stop.\n")

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

        response = taran.respond(user_input)
        print(f"Taran: {response}\n")


if __name__ == "__main__":
    main()
