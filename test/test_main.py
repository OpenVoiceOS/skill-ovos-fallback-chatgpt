from time import sleep
from unittest.mock import Mock, MagicMock
import pytest
from ovos_utils.fakebus import FakeBus

from skill_ovos_fallback_chatgpt import ChatGPTSkill, DEFAULT_SETTINGS


class TestChatGPTSkill:
    bus = FakeBus()
    bus.emitter = bus.ee
    bus.run_forever()

    def test_default_no_key(self):
        skill = ChatGPTSkill(bus=self.bus, skill_id="test")
        skill.speak = Mock()
        skill.speak_dialog = Mock()
        skill.play_audio = Mock()
        skill.log = MagicMock()
        while not skill.is_fully_initialized:
            sleep(0.5)
        assert not skill.settings.get("key")
        skill.ask_chatgpt("Will my test pass?")
        skill.log.error.assert_called()
        skill.speak_dialog.assert_not_called()  # no key, we log an error before speaking ever happens
        assert skill.settings.get("persona") == DEFAULT_SETTINGS["persona"]
        assert skill.settings.get("model") == DEFAULT_SETTINGS["model"]

    def test_default_with_key(self):
        skill = ChatGPTSkill(bus=self.bus, skill_id="test", settings={"key": "test"})
        skill.speak = Mock()
        skill.speak_dialog = Mock()
        skill.play_audio = Mock()
        while not skill.is_fully_initialized:
            sleep(0.5)
        assert skill.settings.get("key") == "test"
        assert skill.settings.get("persona") == DEFAULT_SETTINGS["persona"]
        assert skill.settings.get("model") == DEFAULT_SETTINGS["model"]

    def test_overriding_all_settings(self):
        skill = ChatGPTSkill(bus=self.bus, skill_id="test", settings={
            "key": "test",
            "persona": "I am a test persona",
            "model": "gpt-4-nitro"
        })
        skill.speak = Mock()
        skill.speak_dialog = Mock()
        skill.play_audio = Mock()
        while not skill.is_fully_initialized:
            sleep(0.5)
        assert skill.settings.get("key") == "test"
        assert skill.settings.get("persona") == "I am a test persona"
        assert skill.settings.get("model") == "gpt-4-nitro"
        assert skill.settings.get("persona") != DEFAULT_SETTINGS["persona"]
        assert skill.settings.get("model") != DEFAULT_SETTINGS["model"]

if __name__ == "__main__":
    pytest.main()
