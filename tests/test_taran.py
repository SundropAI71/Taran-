"""Tests for Taran AI Droid."""

import sys
import os
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from taran import Taran, VoiceEngine


# Default fixture has voice disabled — fast, no audio hardware needed.
@pytest.fixture()
def taran():
    return Taran(voice_enabled=False)


# Fixture with a fully mocked pyttsx3 engine.
@pytest.fixture()
def mock_pyttsx3():
    engine = MagicMock()
    engine.getProperty.side_effect = lambda prop: (
        [] if prop == "voices" else (200 if prop == "rate" else 1.0)
    )
    with patch("pyttsx3.init", return_value=engine):
        yield engine


@pytest.fixture()
def taran_voiced(mock_pyttsx3):
    return Taran(voice_enabled=True)


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


class TestAbilities:
    @pytest.mark.parametrize("query", [
        "what are your abilities?",
        "what can you do?",
        "list your abilities",
        "what are your capabilities?",
        "what are your skills?",
        "what are you capable of?",
    ])
    def test_ability_query_triggers_response(self, taran, query):
        response = taran.respond(query)
        # Every ability name must appear in the response
        for ability in taran.abilities():
            assert ability["name"] in response, (
                f"Expected '{ability['name']}' in abilities response, got: {response[:80]}"
            )

    def test_abilities_method_returns_list(self, taran):
        result = taran.abilities()
        assert isinstance(result, list)
        assert len(result) > 0

    def test_abilities_entries_have_required_keys(self, taran):
        for ability in taran.abilities():
            assert "emoji" in ability
            assert "name" in ability
            assert "description" in ability
            assert "examples" in ability

    def test_abilities_method_returns_copy(self, taran):
        first = taran.abilities()
        first.clear()
        assert len(taran.abilities()) > 0

    def test_abilities_response_lists_all_abilities(self, taran):
        response = taran.respond("what are your abilities?")
        for ability in taran.abilities():
            assert ability["name"] in response


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


# ---------------------------------------------------------------------------
# Voice engine tests
# ---------------------------------------------------------------------------

class TestVoiceEngineCleanForSpeech:
    def test_strips_emoji(self):
        result = VoiceEngine._clean_for_speech("Hello! 🤖")
        assert "🤖" not in result
        assert "Hello" in result

    def test_strips_markdown(self):
        result = VoiceEngine._clean_for_speech("**bold** and `code`")
        assert "*" not in result
        assert "`" not in result
        assert "bold" in result
        assert "code" in result

    def test_collapses_whitespace(self):
        result = VoiceEngine._clean_for_speech("hello   world")
        assert result == "hello world"

    def test_empty_string(self):
        assert VoiceEngine._clean_for_speech("") == ""

    def test_plain_text_unchanged(self):
        result = VoiceEngine._clean_for_speech("Roll out")
        assert result == "Roll out"


class TestVoiceEngineInit:
    def test_available_when_pyttsx3_works(self, mock_pyttsx3):
        ve = VoiceEngine()
        assert ve.available is True

    def test_not_available_when_pyttsx3_missing(self):
        with patch("pyttsx3.init", side_effect=Exception("no TTS")):
            ve = VoiceEngine()
        assert ve.available is False

    def test_rate_is_set(self, mock_pyttsx3):
        VoiceEngine()
        mock_pyttsx3.setProperty.assert_any_call("rate", VoiceEngine.RATE)

    def test_volume_is_set(self, mock_pyttsx3):
        VoiceEngine()
        mock_pyttsx3.setProperty.assert_any_call("volume", VoiceEngine.VOLUME)

    def test_preferred_voice_selected_when_available(self):
        voice = MagicMock()
        voice.id = VoiceEngine.PREFERRED_VOICES[0]
        engine = MagicMock()
        engine.getProperty.side_effect = lambda p: (
            [voice] if p == "voices" else 200
        )
        with patch("pyttsx3.init", return_value=engine):
            VoiceEngine()
        engine.setProperty.assert_any_call("voice", VoiceEngine.PREFERRED_VOICES[0])

    def test_fallback_to_en_voice_when_preferred_missing(self):
        voice = MagicMock()
        voice.id = "gmw/en-us-nyc"   # in PREFERRED_VOICES list, not a custom variant
        # Use a voice ID that contains "en" but is NOT in PREFERRED_VOICES
        voice.id = "gmw/en-gb-x-gbclan"
        engine = MagicMock()
        engine.getProperty.side_effect = lambda p: (
            [voice] if p == "voices" else 200
        )
        with patch("pyttsx3.init", return_value=engine):
            VoiceEngine()
        engine.setProperty.assert_any_call("voice", "gmw/en-gb-x-gbclan")


class TestVoiceEngineSpeak:
    def test_speak_calls_say_and_runandwait(self, mock_pyttsx3):
        ve = VoiceEngine()
        ve.speak("Roll out!")
        mock_pyttsx3.say.assert_called_once()
        mock_pyttsx3.runAndWait.assert_called_once()

    def test_speak_returns_true_on_success(self, mock_pyttsx3):
        ve = VoiceEngine()
        assert ve.speak("Autobots!") is True

    def test_speak_returns_false_when_unavailable(self):
        with patch("pyttsx3.init", side_effect=Exception("no TTS")):
            ve = VoiceEngine()
        assert ve.speak("test") is False

    def test_speak_returns_false_for_empty_text(self, mock_pyttsx3):
        ve = VoiceEngine()
        assert ve.speak("") is False

    def test_speak_strips_emoji_before_saying(self, mock_pyttsx3):
        ve = VoiceEngine()
        ve.speak("Hello 🤖")
        spoken = mock_pyttsx3.say.call_args[0][0]
        assert "🤖" not in spoken
        assert "Hello" in spoken

    def test_speak_returns_false_on_engine_error(self, mock_pyttsx3):
        mock_pyttsx3.say.side_effect = RuntimeError("audio error")
        ve = VoiceEngine()
        assert ve.speak("test") is False


class TestTaranVoiceProperty:
    def test_voice_disabled_by_default_fixture(self, taran):
        assert taran.voice_enabled is False

    def test_voice_enabled_with_mock(self, taran_voiced):
        assert taran_voiced.voice_enabled is True

    def test_voice_enabled_false_when_explicitly_disabled(self):
        t = Taran(voice_enabled=False)
        assert t.voice_enabled is False


class TestTaranSpeak:
    def test_speak_returns_false_when_voice_disabled(self, taran):
        assert taran.speak("hello") is False

    def test_speak_delegates_to_voice_engine(self, taran_voiced, mock_pyttsx3):
        taran_voiced.speak("Autobots, roll out!")
        mock_pyttsx3.say.assert_called_once()

    def test_speak_returns_false_when_muted(self, taran_voiced):
        taran_voiced._voice_muted = True
        assert taran_voiced.speak("hello") is False


class TestRespondAndSpeak:
    def test_returns_text_response(self, taran):
        result = taran.respond_and_speak("hello")
        assert len(result) > 0

    def test_records_history(self, taran):
        taran.respond_and_speak("hello")
        assert len(taran.conversation_history) == 2

    def test_speaks_when_voice_enabled(self, taran_voiced, mock_pyttsx3):
        taran_voiced.respond_and_speak("hello")
        mock_pyttsx3.say.assert_called_once()


class TestVoiceCommands:
    def test_mute_command_disables_voice(self, taran_voiced):
        taran_voiced.respond("mute")
        assert taran_voiced._voice_muted is True

    def test_unmute_command_enables_voice(self, taran_voiced):
        taran_voiced._voice_muted = True
        taran_voiced.respond("unmute")
        assert taran_voiced._voice_muted is False

    @pytest.mark.parametrize("cmd", ["mute", "silence", "voice off"])
    def test_mute_variants(self, taran_voiced, cmd):
        taran_voiced.respond(cmd)
        assert taran_voiced._voice_muted is True

    @pytest.mark.parametrize("cmd", ["unmute", "voice on", "speak up"])
    def test_unmute_variants(self, taran_voiced, cmd):
        taran_voiced._voice_muted = True
        taran_voiced.respond(cmd)
        assert taran_voiced._voice_muted is False

    def test_mute_response_message(self, taran_voiced):
        response = taran_voiced.respond("mute")
        assert "muted" in response.lower() or "silent" in response.lower()

    def test_unmute_response_message(self, taran_voiced):
        taran_voiced._voice_muted = True
        response = taran_voiced.respond("unmute")
        assert "online" in response.lower() or "voice" in response.lower()
