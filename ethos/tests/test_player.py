from ethos.utils import get_audio_url
from ethos.config import get_music_folder
from ethos.player import MusicPlayer
import time
player = MusicPlayer()


def test_set_library():
    assert player.set_library(str(get_music_folder()))

def test_get_library_songs():
    assert player.get_library_songs()

def test_get_online_url():
    query = "System of a Down - Chop suey"
    url = get_audio_url(query)
    assert url

def test_local_player():
    print("Setting up library...")
    success = player.set_library(str(get_music_folder()))
    if success:
        songs = player.get_library_songs()
        print(f"Found {len(songs)} songs in library")

        if songs:
            print("Testing local playback...")
            player.play(songs[0])  # Play the first song in the folder
            time.sleep(1)

            print("Testing volume controls...")
            player.set_volume(50)
            time.sleep(1)
            player.set_volume(100)
            time.sleep(1)

            print("Testing pause/resume...")
            player.pause()
            time.sleep(1)
            player.resume()
            time.sleep(1)
            player.stop()
    assert success

def test_online_player():
    print("\nTesting online playback...")
    query = "System of a Down - Chop suey"
    url = get_audio_url(query)
    if url:
        print(f"Playing {query}...")
        player.play(url)
        time.sleep(1)

        print("Testing volume controls...")
        player.set_volume(50)
        time.sleep(1)
        player.set_volume(100)
        time.sleep(1)

        print("Testing pause/resume...")
        player.pause()
        time.sleep(1)
        player.resume()
        time.sleep(1)
        player.stop()
    assert url

def test_local_player_unsupportted_files():
    print("\nTesting unsupported file types...")
    #file formats that are expected to give error when attempting to play with vlc media player
    unsupported_files = [
        "test.txt",
        "test.exe",
        "test.zip",
        "test.doc",
        "test.pdf",
        "test.jpg",
        "test.png",
    ]
    #file formats that are expected to give no error when attempting to play with vlc media player
    supported_files = [
        "test.mp3",
        "test.mp4",
        "test.wav",
        "test.m4a",
        "test.ogg",
        "test.flac",
    ]
    directory = f"./testing_files"
    for file in unsupported_files:
        playing_status = player.play(f"{directory}/{file}")
        if not playing_status:
            print(f"Playing failed for {file.split(".")[0]}")
        assert not player.play(f"{get_music_folder()}/{file}")

    for file in supported_files:
        playing_status = player.play(f"{directory}/{file}")
        if not playing_status:
            print(f"Playing failed for {file.split(".")[0]}")
        assert player.play(f"{get_music_folder()}/{file}")

    assert player.stop()
