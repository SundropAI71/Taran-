"""Tests for the Taran Flask web application."""

import sys
import os
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import json
import pytest

# Patch pyttsx3 before importing app so VoiceEngine doesn't try to init TTS.
with patch("pyttsx3.init", side_effect=Exception("no TTS")):
    import app as flask_app


@pytest.fixture(autouse=True)
def reset_taran():
    """Reset the shared Taran instance between tests."""
    flask_app._taran = None
    yield
    flask_app._taran = None


@pytest.fixture()
def client():
    flask_app.app.config["TESTING"] = True
    with flask_app.app.test_client() as c:
        yield c


# ---------------------------------------------------------------------------
# Index page
# ---------------------------------------------------------------------------

class TestIndexRoute:
    def test_returns_200(self, client):
        resp = client.get("/")
        assert resp.status_code == 200

    def test_contains_taran_name(self, client):
        resp = client.get("/")
        assert b"Taran" in resp.data

    def test_contains_version(self, client):
        resp = client.get("/")
        assert flask_app.Taran.VERSION.encode() in resp.data

    def test_content_type_html(self, client):
        resp = client.get("/")
        assert "text/html" in resp.content_type


# ---------------------------------------------------------------------------
# /chat endpoint
# ---------------------------------------------------------------------------

class TestChatRoute:
    def test_returns_200(self, client):
        resp = client.post("/chat", json={"message": "hello"})
        assert resp.status_code == 200

    def test_response_is_json(self, client):
        resp = client.post("/chat", json={"message": "hello"})
        data = resp.get_json()
        assert data is not None
        assert "response" in data

    def test_response_is_string(self, client):
        resp = client.post("/chat", json={"message": "hello"})
        assert isinstance(resp.get_json()["response"], str)

    def test_non_empty_response(self, client):
        resp = client.post("/chat", json={"message": "tell me a joke"})
        assert len(resp.get_json()["response"]) > 0

    def test_empty_message_returns_prompt(self, client):
        resp = client.post("/chat", json={"message": ""})
        body = resp.get_json()["response"]
        assert len(body) > 0

    def test_missing_message_key(self, client):
        resp = client.post("/chat", json={})
        assert resp.status_code == 200
        assert "response" in resp.get_json()

    def test_no_json_body(self, client):
        resp = client.post("/chat", data="not json", content_type="text/plain")
        assert resp.status_code == 200

    def test_math_expression(self, client):
        resp = client.post("/chat", json={"message": "2 + 2"})
        assert "4" in resp.get_json()["response"]

    def test_greeting_response(self, client):
        resp = client.post("/chat", json={"message": "hello"})
        assert resp.status_code == 200
        assert len(resp.get_json()["response"]) > 0

    def test_abilities_query(self, client):
        resp = client.post("/chat", json={"message": "what can you do?"})
        text = resp.get_json()["response"]
        assert "abilities" in text.lower() or "Greetings" in text


# ---------------------------------------------------------------------------
# /history endpoint
# ---------------------------------------------------------------------------

class TestHistoryRoute:
    def test_returns_200(self, client):
        assert client.get("/history").status_code == 200

    def test_returns_list(self, client):
        data = client.get("/history").get_json()
        assert isinstance(data["history"], list)

    def test_history_grows_after_chat(self, client):
        client.post("/chat", json={"message": "hello"})
        data = client.get("/history").get_json()
        assert len(data["history"]) == 2


# ---------------------------------------------------------------------------
# /clear endpoint
# ---------------------------------------------------------------------------

class TestClearRoute:
    def test_returns_200(self, client):
        assert client.post("/clear").status_code == 200

    def test_clears_history(self, client):
        client.post("/chat", json={"message": "hello"})
        client.post("/clear")
        data = client.get("/history").get_json()
        assert data["history"] == []

    def test_returns_cleared_status(self, client):
        data = client.post("/clear").get_json()
        assert data["status"] == "cleared"


# ---------------------------------------------------------------------------
# /abilities endpoint
# ---------------------------------------------------------------------------

class TestAbilitiesRoute:
    def test_returns_200(self, client):
        assert client.get("/abilities").status_code == 200

    def test_returns_list(self, client):
        data = client.get("/abilities").get_json()
        assert isinstance(data["abilities"], list)
        assert len(data["abilities"]) > 0

    def test_each_ability_has_required_fields(self, client):
        data = client.get("/abilities").get_json()
        for ability in data["abilities"]:
            assert "emoji" in ability
            assert "name" in ability
            assert "description" in ability
            assert "examples" in ability
