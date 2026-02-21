"""
Taran Web App — Android Intelligence and Logic with Humor AI Droid.

Run:
    python app.py

Then open http://localhost:5000 in your browser (or on any device on the
same network at http://<your-ip>:5000).
"""

import io
import os
import socket

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


def _get_local_ip() -> str:
    """Return the machine's LAN IP address, or '127.0.0.1' as fallback."""
    try:
        # Connect to an external address (no data sent) to find the outbound interface.
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"


def _make_qr_ascii(url: str) -> str:
    """Return an ASCII QR code string for *url*."""
    try:
        import qrcode
        qr = qrcode.QRCode(border=1)
        qr.add_data(url)
        qr.make(fit=True)
        buf = io.StringIO()
        qr.print_ascii(out=buf, invert=True)
        return buf.getvalue()
    except Exception:
        return ""


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    """Serve the main chat page."""
    taran = _get_taran()
    intro = taran.introduce()
    local_ip = _get_local_ip()
    mobile_url = f"http://{local_ip}:5000"
    qr_ascii = _make_qr_ascii(mobile_url)
    return render_template(
        "index.html",
        intro=intro,
        version=Taran.VERSION,
        mobile_url=mobile_url,
        qr_ascii=qr_ascii,
    )


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


@app.route("/access", methods=["GET"])
def access():
    """Return access URLs and a QR code for mobile/Android.

    Response (JSON):
        {
            "local_url":  "http://127.0.0.1:5000",
            "mobile_url": "http://192.168.x.x:5000",
            "qr_ascii":   "... ASCII QR code ..."
        }
    """
    local_ip = _get_local_ip()
    mobile_url = f"http://{local_ip}:5000"
    return jsonify({
        "local_url": "http://127.0.0.1:5000",
        "mobile_url": mobile_url,
        "qr_ascii": _make_qr_ascii(mobile_url),
    })


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    local_ip = _get_local_ip()
    mobile_url = f"http://{local_ip}:5000"

    print(f"\n🤖  Taran v{Taran.VERSION} is online!\n")
    _BOX_WIDTH = 45
    _inner = _BOX_WIDTH - 2  # width inside the border characters
    mobile_label = f"      {mobile_url}"

    print("┌" + "─" * _inner + "┐")
    print("│" + "  HOW TO ACCESS TARAN".ljust(_inner) + "│")
    print("│" + " " * _inner + "│")
    print("│" + "  💻  On this computer:".ljust(_inner) + "│")
    print("│" + "      http://localhost:5000".ljust(_inner) + "│")
    print("│" + " " * _inner + "│")
    print("│" + "  📱  On Android / phone (same Wi-Fi):".ljust(_inner) + "│")
    print("│" + mobile_label.ljust(_inner) + "│")
    print("│" + " " * _inner + "│")
    print("│" + "  📷  Scan the QR code below on your phone:".ljust(_inner) + "│")
    print("└" + "─" * _inner + "┘\n")

    qr_ascii = _make_qr_ascii(mobile_url)
    if qr_ascii:
        print(qr_ascii)

    print("   Press Ctrl+C to stop.")
    print("   ⚠️  For production use, run with a WSGI server (e.g. gunicorn app:app).\n")
    app.run(host="0.0.0.0", port=5000, debug=False)
