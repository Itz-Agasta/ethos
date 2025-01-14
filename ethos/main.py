####################
# Temporary script #
####################
from player import MusicPlayer, TrackInfo
from utils import get_audio_url, get_song_metadata
from config import get_music_folder, ConfigManager
import time
import asyncio
from datetime import timedelta

def test_player():
    """
    Temporary function that tests the functionality of the MusicPlayer class.

    This function performs a sequence of tests to validate the behavior of the
    `MusicPlayer` class, including testing playback of songs from a local library and
    online resources. In addition, it verifies various features like setting volume levels
    and controlling playback via pause, resume, and stop operations.

    The function is divided into two main parts:
    1. Testing the library functionality: It initializes a local music library,
       retrieves the available songs, and tests playback along with volume and playback
       controls.
    2. Testing the online playback functionality: It queries for a specific audio track
       URL, plays it, and validates volume and playback controls.

    """
    player = MusicPlayer()

    config_manager = ConfigManager()

    # config_manager.delete_config()
    
    # Test local library
    print("Setting up library...")
    success = player.set_library(str(get_music_folder()))
    if success:
        songs = player.get_library_songs()
        print(f"Found {len(songs)} songs in library")
        
        if songs:
            print("Testing local playback...")   # Took 2.23 sec.
            duration = TrackInfo.get_audio_duration(songs[0])
            print(f"Duration of the song: {duration} seconds")
            # print(f"Duration of the song: {formate.seconds_to_min_sec(duration)}")

            player.play(songs[0]) # Play the first song in the folder
            time.sleep(5) 

            print("Testing volume controls...")
            player.set_volume(50)
            time.sleep(2)
            
            current_time = TrackInfo.get_current_time(player)
            progress = TrackInfo.get_progress(player)

            print(f"Current playback time: {current_time} seconds")
            print(f"Playback progress: {progress:.2f}%")



            player.set_volume(100)
            time.sleep(2)
            
            print("Testing pause/resume...")
            player.pause()
            time.sleep(2)
            player.resume()
            time.sleep(5)
            player.stop()

    # config_manager.rewrite_config()

    # Test online playback
    print("\nTesting online playback...") # Took 4.40 sec.
    query = "sky-fall"
    url = get_audio_url(query)
    if url:
        print(f"Playing {query}...")
        player.play(url)
        time.sleep(10)

        print("Testing volume controls...")
        player.set_volume(50)
        time.sleep(5)
        player.set_volume(100)
        time.sleep(2)

        print("Testing pause/resume...")
        player.pause()
        time.sleep(2)
        player.resume()

        time.sleep(150)        
        current_time = TrackInfo.get_current_time(player)
        progress = TrackInfo.get_progress(player)

        print(f"Current playback time: {current_time} seconds")
        print(f"Playback progress: {progress:.2f}%")
        player.stop()

        # Test get_song_metadata function
        print("\nTesting get_song_metadata function...") # Took 8 sec.
        start_time = time.monotonic()
        metadata =asyncio.run(get_song_metadata(query))
        end_time = time.monotonic()
        print(f"you were playing: {metadata}")
        print( timedelta(seconds=end_time - start_time))

if __name__ == "__main__":
    test_player()
