"""Tests for Taran AI Droid."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from taran import Taran


@pytest.fixture()
def taran():
    return Taran()


class TestIntroduction:
    def test_introduce_contains_name(self, taran):
        intro = taran.introduce()
        assert "Taran" in intro

    def test_introduce_contains_version(self, taran):
        intro = taran.introduce()
        assert taran.VERSION in intro


class TestGreetings:
    @pytest.mark.parametrize("greeting", ["hello", "hi", "hey", "greetings"])
    def test_greeting_response(self, taran, greeting):
        response = taran.respond(greeting)
        assert "Taran" in response or "morning" in response.lower() \
               or "afternoon" in response.lower() or "evening" in response.lower()


class TestFarewells:
    @pytest.mark.parametrize("farewell", ["bye", "goodbye", "farewell"])
    def test_farewell_response(self, taran, farewell):
        response = taran.respond(farewell)
        assert len(response) > 0


class TestHumor:
    def test_joke_request(self, taran):
        response = taran.respond("tell me a joke")
        assert len(response) > 0

    def test_funny_request(self, taran):
        response = taran.respond("say something funny")
        assert len(response) > 0


class TestTime:
    def test_time_request(self, taran):
        response = taran.respond("what time is it?")
        assert len(response) > 0

    def test_date_request(self, taran):
        response = taran.respond("what is the date today?")
        assert len(response) > 0


class TestMath:
    def test_addition(self, taran):
        response = taran.respond("2 + 2")
        assert "4" in response

    def test_multiplication(self, taran):
        response = taran.respond("6 * 7")
        assert "42" in response

    def test_invalid_math(self, taran):
        response = taran.respond("abc + xyz")
        assert len(response) > 0


class TestHelp:
    def test_help_response(self, taran):
        response = taran.respond("help")
        assert len(response) > 0


class TestIdentity:
    def test_who_are_you(self, taran):
        response = taran.respond("who are you?")
        assert "Taran" in response

    def test_version(self, taran):
        response = taran.respond("what version are you?")
        assert taran.VERSION in response


class TestConversationHistory:
    def test_history_recorded(self, taran):
        taran.respond("hello")
        history = taran.conversation_history
        assert len(history) == 2
        assert history[0]["role"] == "user"
        assert history[1]["role"] == "taran"

    def test_clear_history(self, taran):
        taran.respond("hi")
        taran.clear_history()
        assert taran.conversation_history == []

    def test_history_is_copy(self, taran):
        taran.respond("hi")
        history = taran.conversation_history
        history.clear()
        assert len(taran.conversation_history) == 2


class TestEdgeCases:
    def test_empty_input(self, taran):
        response = taran.respond("")
        assert len(response) > 0

    def test_whitespace_only_input(self, taran):
        response = taran.respond("   ")
        assert len(response) > 0

    def test_default_response(self, taran):
        response = taran.respond("zxqwerty random stuff 12345")
        assert len(response) > 0
