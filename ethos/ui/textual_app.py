from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import Input
from textual import work
from ethos.ui.rich_layout import RichLayout
from ethos.player import MusicPlayer, TrackInfo
from ethos.tools import helper
from ethos.utils import Search, UserFiles
import random

class TextualApp(App):
    """Textual Application Class for ethos UI"""

    CSS_PATH = "./styles.tcss"

    BINDINGS = [
        ("ctrl+c", "quit", "Quit"),
        ("ctrl+q", "quit", "Quit"),
        ("ctrl+m", "pause", "Pause"),
        ("ctrl+r", "resume", "Resume"),
        ("ctrl+1", "volume_up"),
        ("ctrl+2", "volume_down")
    ]

    player = MusicPlayer()
    tracks_list = reactive([])
    track_to_play = reactive("")
    helper = helper.Format()
    queue = reactive({})
    queue_options = reactive([])
    search_track = reactive("")
    select_from_queue = reactive("")
    track_url = reactive("")
    volume = reactive(50)
    should_play_queue = reactive(False)
    recents = reactive([])
    current_track_duration = reactive("")
    show_playlists = reactive(False)
    layout_widget = ""
    current_playlist = reactive("")
    add_playlist = reactive(False)


    def compose(self) -> ComposeResult:
        """Composer function for textual app"""

        yield RichLayout(id="rich-layout-widget")
        yield Input(placeholder="Type a command")


    def on_mount(self):
        """Handle functions after mounting the app"""

        self.input = reactive("")
        self.recents = UserFiles.fetch_recents()
        self.layout_widget = self.query_one(RichLayout)

        try:
            if self.recents:
                self.layout_widget.update_dashboard(self.recents, "Recents :-")
            else:
                self.layout_widget.update_dashboard("You have not played any tracks yet!", "")
            self.set_interval(1, self.update_)
        except:
            pass

    @work
    async def on_input_submitted(self, event: Input.Submitted):
        """Handle input submission"""

        self.input = event.value
        
        
        if event.value:
            if event.value.startswith("/play"):
                try:
                    search_track = self.helper.parse_command(event.value)
                    self.layout_widget.update_log("Searching for tracks")
                    self.tracks_list = await Search.fetch_tracks_list(search_track)
                    if self.tracks_list:
                        self.layout_widget.update_dashboard(self.tracks_list, "Type track no. to be played :-")
                        self.update_input()
                        self.select_from_queue = False
                except ValueError:
                    self.layout_widget.update_dashboard("Invalid command. Make sure to enter a valid command. You can see the list of commands using /help", "")
                    pass
                    

            if event.value.isdigit() and not self.select_from_queue and not self.add_playlist:
                try:
                    self.should_play_queue = False
                    self.track_to_play = self.tracks_list[int(event.value)-1]
                    self.handle_play(self.track_to_play)
                    self.layout_widget.update_log("Playing track from search")
                    self.update_input()
                except:
                    pass

            if event.value.startswith("/volume"):
                try:
                    volume_to_be_set = self.helper.parse_command(event.value)
                    self.player.set_volume(volume_to_be_set)
                    self.update_input()
                    self.layout_widget.update_volume(volume_to_be_set)
                except ValueError:
                    self.layout_widget.update_dashboard("Please enter the volume in digits.", "")
                    pass
            
            if event.value.startswith("/queue-add"):
                try:
                    self.search_track = self.helper.parse_command(event.value)
                    self.queue_options = await Search.fetch_tracks_list(self.search_track)
                    if self.queue_options:
                        self.layout_widget.update_dashboard(self.queue_options, "Type track no. to be added to queue :-")
                        self.update_input()
                        self.select_from_queue = True
                except ValueError:
                    self.layout_widget.update_dashboard("Please enter a valid track name. You can view the list of commands using /help", "")
                    pass

            if event.value.isdigit() and self.select_from_queue and not self.add_playlist:
                try:
                    self.should_play_queue = True
                    self.track_to_be_added_to_queue = self.queue_options[int(event.value)-1]
                    self.queue[self.search_track] = helper.Format.clean_hashtag(self.track_to_be_added_to_queue)
                    self.update_input()
                    self.search_track=""
                except:
                    pass

            if event.value.startswith("/show-queue"):
                try:
                    tracks = self.queue.values()
                    data = "\n".join(f"{i+1}. {track}" for i, track in enumerate(tracks))
                    self.layout_widget.update_dashboard(data, "Current Queue :-")
                    self.update_input()
                except:
                    pass

            if event.value.startswith("/pause"):
                self.action_pause()

            if event.value.startswith("/resume"):
                self.action_resume()

            if event.value.startswith("/qp"):
                try:
                    ind = int(helper.Format.parse_command(event.value))
                    keys = list(self.queue.keys())
                    key = keys[ind-1]
                    queue = list(self.queue.values())
                    track = queue[ind-1]
                    del self.queue[key]
                    self.handle_play(track)
                    self.layout_widget.update_log("Playing track from current queue")
                    self.update_input()
                except ValueError:
                    self.layout_widget.update_dashboard("Please enter the no. of track you want to play", "")
                    pass
            
            if event.value == "/recents":
                try:
                    self.recents = UserFiles.fetch_recents()
                    self.layout_widget.update_dashboard(self.recents, "Recents :")
                    self.update_input()
                except:
                    pass

            if event.value == "/sp" or event.value == "/show-playlists":
                self.show_playlists()

            if event.value.startswith("/ap"):
                try:
                    self.current_playlist, track_name = self.helper.parse_command(event.value)
                    self.tracks_list = await Search.fetch_tracks_list(track_name)
                    self.layout_widget.update_dashboard(self.tracks_list, f"Enter track number to be added to {self.current_playlist}")
                    self.add_playlist = True
                    self.update_input()
                except:
                    pass
            
            if event.value.isdigit() and self.add_playlist:
                try:
                    track_name = self.tracks_list[event.value - 1]
                    UserFiles.add_track_to_playlist(self.current_playlist, track_name)
                    self.update_input()
                except:
                    pass
            
            if event.value.startswith("/vp"):
                playlist_name = self.helper.parse_command(event.value)
                self.show_tracks_from_playlist(playlist_name)
                self.update_input()
            
            if event.value == "/recents":
                try:
                    self.recents = UserFiles.fetch_recents()
                    self.layout_widget.update_dashboard(self.recents, "Recents :")
                    self.update_input()
                except:
                    pass

            if event.value == "/sp" or event.value == "/show-playlists":
                self.show_playlists()

            if event.value.startswith("/ap"):
                playlist_name, track_name = self.helper.parse_command(event.value)
                self.add_to_playlist(track_name, playlist_name)

            if event.value.startswith("/vp"):
                playlist_name = self.helper.parse_command(event.value)
                self.show_tracks_from_playlist(playlist_name)

    
            if event.value == "/help":
                try:
                    self.layout_widget.show_commands()
                except:
                    pass
            

    def action_pause(self):
        """Pause the player"""
        self.player.pause()
        self.layout_widget.update_playing_status()


    def action_resume(self):
        """Resume the player"""
        
        if not self.player.is_playing:
            self.player.resume()
            self.layout_widget.update_playing_status()

    def action_volume_up(self):
        """Increase the volume by 5 levels"""
        current_volume = self.player.get_volume()
        self.player.set_volume(current_volume+5)
        self.layout_widget.update_volume(self.player.get_volume())

    def action_volume_down(self):
        """Decrease the volume by 5 levels"""
        current_volume = self.player.get_volume()
        self.player.set_volume(current_volume-5)
        self.layout_widget.update_volume(self.player.get_volume())

    def handle_play(self, track_name: str):
        """Function to handle the track playback"""
        try:
            url = Search.get_audio_url(track_name+" official music video")
            self.track_url = url
            self.player.set_volume(50)
            self.player.play(url)
            UserFiles.add_track_to_recents(helper.Format.clean_hashtag(track_name))
            self.layout_widget.update_track(track_name)
            self.current_track_duration = TrackInfo.get_audio_duration(url)
            self.layout_widget.update_total_track_time(TrackInfo.get_audio_duration(url))
            color_ind = random.randint(0,9)
            self.layout_widget.update_color(color_ind)
        except:
            pass
    
    def show_playlists(self) -> None:
        try:
            playlists = UserFiles.fetch_playlists()
            data = "\n".join(playlists) if playlists else ""
            self.layout_widget.update_dashboard(data, "Your playlists")
        except:
            pass

    def show_tracks_from_playlist(self, playlist: str) -> None:
        try:
            playlist = UserFiles.fetch_tracks_from_playlist(playlist)
            data = "\n".join(f"{i+1}. {track}" for i, track in enumerate(playlist))
            self.layout_widget.update_dashboard(data, "Playlist Contents :")
        except:
            pass


    def show_tracks_from_playlist(self, playlist: str) -> None:
        try:
            playlist = UserFiles.fetch_tracks_from_playlist(playlist)
            data = "\n".join(f"{i+1}. {track}" for i, track in enumerate(playlist))
            self.layout_widget.update_dashboard(data, "Playlist Contents :")
        except:
            pass


    def add_to_playlist(self, track, playlist: str) -> None:
        try:
            UserFiles.add_track_to_playlist(track, playlist)
            self.layout_widget.update_log("Track added to playlist")
        except:
            pass
            

    def update_input(self) -> None:
        """Function to reset the data in input widget once user enters his input"""
        input_widget = self.query_one(Input)
        input_widget.placeholder = ""
        input_widget.value = ""
    
    def update_(self) -> None:
        """Function to update track progress and check for queue"""
        
        try:   
            self.layout_widget.update_music_progress(TrackInfo.get_current_time(self.player), int(TrackInfo.get_progress(self.player)))
        except:
            pass

        if TrackInfo.get_progress(self.player) == 100.0:
            if self.queue:
                try:
                    keys = list(self.queue.keys())
                    tracks = list(self.queue.values())
                    key = keys[0]
                    track = tracks[0]
                    del self.queue[key]
                    self.handle_play(track)
                    entries = self.queue.values()
                    data = "\n".join(f"{i+1}. {track}" for i, track in enumerate(entries))
                    self.layout_widget.update_dashboard(data, "Current Queue :-")
                    self.layout_widget.update_log("Currently playing from queue")
                except:
                    pass

  
    
