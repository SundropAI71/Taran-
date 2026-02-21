"""
Taran Web App — Android Intelligence and Logic with Humor AI Droid.

Run:
    python app.py

Then open http://localhost:5000 in your browser (or on any device on the
same network at http://<your-ip>:5000).
"""

import os

from flask import Flask, jsonify, render_template, request, session

from taran import Taran

app = Flask(__name__)
# Load secret key from environment; fall back to a dev-only default.
# In production set the SECRET_KEY environment variable to a long random string.
app.secret_key = os.environ.get("SECRET_KEY", "taran-dev-secret-change-in-production")

# One Taran instance per user session, keyed by Flask session ID.
# For simplicity we keep a single global instance (sufficient for local use).
_taran: Taran | None = None


def _get_taran() -> Taran:
    """Return (or lazily create) the shared Taran instance."""
    global _taran
    if _taran is None:
        _taran = Taran(voice_enabled=False)  # voice is managed client-side in the app
    return _taran


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    """Serve the main chat page."""
    taran = _get_taran()
    intro = taran.introduce()
    return render_template("index.html", intro=intro, version=Taran.VERSION)


@app.route("/chat", methods=["POST"])
def chat():
    """Accept a user message and return Taran's response as JSON.

    Request body (JSON): {"message": "..."}
    Response (JSON):     {"response": "..."}
    """
    data = request.get_json(silent=True) or {}
    user_message = str(data.get("message", "")).strip()
    if not user_message:
        return jsonify({"response": "I'm listening… say something! 😄"})

    taran = _get_taran()
    response = taran.respond(user_message)
    return jsonify({"response": response})


@app.route("/history", methods=["GET"])
def history():
    """Return the full conversation history as JSON."""
    taran = _get_taran()
    return jsonify({"history": taran.conversation_history})


@app.route("/clear", methods=["POST"])
def clear():
    """Clear the conversation history."""
    taran = _get_taran()
    taran.clear_history()
    return jsonify({"status": "cleared"})


@app.route("/abilities", methods=["GET"])
def abilities():
    """Return Taran's abilities catalogue as JSON."""
    taran = _get_taran()
    return jsonify({"abilities": taran.abilities()})


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print(f"🤖 Taran v{Taran.VERSION} — starting web app…")
    print("   Open http://localhost:5000 in your browser.")
    print("   On mobile / Android: http://<your-local-ip>:5000")
    print("   Press Ctrl+C to stop.")
    print("   ⚠️  For production use, run with a WSGI server (e.g. gunicorn app:app).\n")
    app.run(host="0.0.0.0", port=5000, debug=False)
