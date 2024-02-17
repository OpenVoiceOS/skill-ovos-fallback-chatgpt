import shutil
from os import environ, getenv
from os.path import dirname, join
from threading import Event
from time import sleep
from unittest import TestCase
from unittest.mock import MagicMock, Mock

import pytest
from ovos_utils.fakebus import FakeBus
from skill_ovos_fallback_chatgpt import DEFAULT_SETTINGS, ChatGPTSkill


class TestChatGPTSkill(TestCase):
    # Define test directories
    test_fs = join(dirname(__file__), "skill_fs")
    data_dir = join(test_fs, "data")
    conf_dir = join(test_fs, "config")
    environ["XDG_DATA_HOME"] = data_dir
    environ["XDG_CONFIG_HOME"] = conf_dir

    bus = FakeBus()
    bus.emitter = bus.ee
    bus.connected_event = Event()
    bus.connected_event.set()
    bus.run_forever()
    test_skill_id = 'test_skill.test'
    
    skill = None

    @classmethod
    def setUpClass(cls) -> None:
        # Get test skill
        cls.skill = ChatGPTSkill(skill_id=cls.test_skill_id, bus=cls.bus)
        # Override speak and speak_dialog to test passed arguments
        cls.skill.speak = Mock()
        cls.skill.speak_dialog = Mock()

    def setUp(self):
        self.skill.speak.reset_mock()
        self.skill.speak_dialog.reset_mock()
        self.skill.play_audio = Mock()
        self.skill.log = MagicMock()

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(cls.test_fs)

    def test_default_no_key(self):
        assert not self.skill.settings.get("key")
        self.skill.ask_chatgpt("Will my test pass?")
        self.skill.log.error.assert_called()
        self.skill.speak_dialog.assert_not_called()  # no key, we log an error before speaking ever happens
        assert self.skill.settings.get("persona") == DEFAULT_SETTINGS["persona"]
        assert self.skill.settings.get("model") == DEFAULT_SETTINGS["model"]

    def test_default_with_key(self):
        self.skill.settings["key"] = "test"
        self.skill.settings.store()
        assert self.skill.settings.get("key") == "test"
        assert self.skill.settings.get("persona") == DEFAULT_SETTINGS["persona"]
        assert self.skill.settings.get("model") == DEFAULT_SETTINGS["model"]

    def test_overriding_all_settings(self):
        self.skill.settings["key"] = "test"
        self.skill.settings["persona"] = "I am a test persona"
        self.skill.settings["model"] = "gpt-4-nitro"
        self.skill.settings.store()
        assert self.skill.settings.get("key") == "test"
        assert self.skill.settings.get("persona") == "I am a test persona"
        assert self.skill.settings.get("model") == "gpt-4-nitro"
        assert self.skill.settings.get("persona") != DEFAULT_SETTINGS["persona"]
        assert self.skill.settings.get("model") != DEFAULT_SETTINGS["model"]

if __name__ == "__main__":
    pytest.main()
