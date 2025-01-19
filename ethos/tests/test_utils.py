from ethos.utils import get_song_metadata, get_audio_url


def test_get_song_metadata():
    assert get_song_metadata("System of a Down - Chop suey")

def test_get_audio_url():
    assert get_audio_url("System of a Down - Chop suey")
