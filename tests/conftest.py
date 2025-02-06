import pytest
import vlc
from pathlib import Path
from ethos.player import MusicPlayer

# --- Dummy VLC Classes for Testing --- #

class DummyMedia:
    def __init__(self, path):
        self.path = path
        self.duration = 10000  

    def get_duration(self):
        return self.duration

class DummyPlayer:
    def __init__(self):
        self.volume = 50
        self.time = 0
        self.media = None

    def set_media(self, media):
        self.media = media

    def play(self):
        
        pass

    def pause(self):
        pass

    def stop(self):
        self.media = None

    def audio_set_volume(self, volume):
        self.volume = volume

    def audio_get_volume(self):
        return self.volume

    def get_state(self):
        return "DummyState"

    def get_time(self):
        return self.time

    def set_time(self, new_time):
        self.time = new_time

    def get_media(self):
        return self.media

class DummyVLCInstance:
    def media_new(self, path):
        return DummyMedia(path)

    def media_player_new(self):
        return DummyPlayer()

# --- Fixtures --- #

@pytest.fixture
def music_player(monkeypatch):
    """
    Fixture that patches vlc.Instance to use DummyVLCInstance.
    """
    monkeypatch.setattr(vlc, "Instance", lambda: DummyVLCInstance())
    return MusicPlayer()

