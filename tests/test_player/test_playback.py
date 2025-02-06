import pytest

@pytest.mark.playback
def test_play(music_player):
    track_path = "dummy_track.mp3"
    result = music_player.play(track_path)
    assert result is True
    assert music_player.current_track == track_path
    assert music_player.is_playing is True

@pytest.mark.playback
def test_pause_resume_stop(music_player):
    track_path = "dummy_track.mp3"
    music_player.play(track_path)
    
    # Test pause
    music_player.pause()
    assert music_player.is_playing is False

    # Test resume
    music_player.resume()
    assert music_player.is_playing is True

    # Test stop
    music_player.stop()
    assert music_player.is_playing is False
    assert music_player.current_track is None

@pytest.mark.playback
def test_skip_forward(music_player):
    track_path = "dummy_track.mp3"
    music_player.play(track_path)
    music_player.player.set_time(2000)  
    music_player.skip_forward(5)  
    # Expected time is 7000 ms (2000 + 5000)
    assert music_player.player.get_time() == 7000

    # Test skipping forward near end of track
    music_player.player.set_time(8000)
    music_player.skip_forward(5)
    # Dummy media duration is 10000 ms, so time should not exceed that
    assert music_player.player.get_time() == 10000

@pytest.mark.playback
def test_skip_backward(music_player):
    track_path = "dummy_track.mp3"
    music_player.play(track_path)
    music_player.player.set_time(5000)
    music_player.skip_backward(3)  
    assert music_player.player.get_time() == 2000

    # Ensure time does not go negative
    music_player.player.set_time(2000)
    music_player.skip_backward(5)
    assert music_player.player.get_time() == 0

@pytest.mark.playback
def test_volume_boundaries(music_player):
    """Test volume limits"""
    music_player.set_volume(-10)  # Should clamp to 0
    assert music_player.get_volume() == 0
    
    music_player.set_volume(150)  # Should clamp to 100
    assert music_player.get_volume() == 100

@pytest.mark.track_info
def test_state_transitions(music_player):
    """Test player state transitions"""
    assert not music_player.is_playing  
    
    music_player.play("dummy_track.mp3")
    assert music_player.is_playing  
    
    music_player.pause()
    assert not music_player.is_playing  

@pytest.mark.track_info
def test_track_info(music_player):
    """Test track information and progress"""
    music_player.play("dummy_track.mp3")
    music_player.player.set_time(5000)  
    
    from ethos.player import TrackInfo
    assert TrackInfo.get_current_time(music_player) == "0:05"