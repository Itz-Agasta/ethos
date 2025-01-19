from unittest import mock
from ethos.config import ConfigManager

def test_get_music_folder_from_env():
    config_manager = ConfigManager()
    assert config_manager.get_music_folder_from_env()

def test_get_music_folder_from_rc():
    config_manager = ConfigManager()
    assert config_manager.get_music_folder_from_rc()
@mock.patch("ethos.config.prompt_user_for_music_folder")
def test_prompt_user_for_music_folder(mock_user_input):
    mock_user_input.return_value = input("Please enter the path to your music folder: ")
    config_manager = ConfigManager()
    assert config_manager.prompt_user_for_music_folder()

def test_fetch_config():
    config_manager = ConfigManager()
    assert config_manager.fetch_config()

@mock.patch("ethos.config.rewrite_config")
def test_rewrite_config(self, user_input_for_music_folder):
    user_input_for_music_folder.return_value = input("Please enter the path to your music folder: ")
    config_manager = ConfigManager()
    current_config = config_manager.fetch_config()
    assert config_manager.rewrite_config() is not current_config

def test_delete_config():
    config_manager = ConfigManager()
    assert config_manager.delete_config()
