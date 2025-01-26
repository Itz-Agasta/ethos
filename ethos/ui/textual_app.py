from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import Input
from textual import work
from ui.rich_layout import RichLayout
from player import MusicPlayer, TrackInfo
from tools import helper
from utils import fetch_tracks_list, get_audio_url, fetch_recents, add_track_to_recents
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

    def compose(self) -> ComposeResult:
        """Composer function for textual app"""

        yield RichLayout(id="rich-layout-widget")
        yield Input(placeholder="Type a command")


    def on_mount(self):
        """Handle functions after mounting the app"""

        self.input = reactive("")
        self.recents = fetch_recents()
        layout_widget = self.query_one(RichLayout)
        if self.recents:
            layout_widget.update_dashboard(self.recents, "Recents :-")
        else:
            layout_widget.update_dashboard("You have not played any tracks yet!", "")
        self.set_interval(1, self.update_track_progress)

    @work
    async def on_input_submitted(self, event: Input.Submitted):
        """Handle input submission"""

        self.input = event.value
        layout_widget = self.query_one(RichLayout)
        
        if event.value:
            if event.value.startswith("/play"):
                search_track = self.helper.parse_command(event.value)
                self.tracks_list = await fetch_tracks_list(search_track)
                if self.tracks_list:
                    layout_widget.update_dashboard(self.tracks_list, "Type track no. to be played :-")
                    self.update_input()
                    self.select_from_queue = False

            if event.value.isdigit() and not self.select_from_queue:
                self.should_play_queue = False
                self.track_to_play = self.tracks_list[int(event.value)-1]
                self.handle_play(self.track_to_play)
                self.update_input()

            if event.value.startswith("/volume"):
                volume_to_be_set = self.helper.parse_command(event.value)
                self.player.set_volume(volume_to_be_set)
                self.update_input()
                layout_widget.update_volume(volume_to_be_set)
            
            if event.value.startswith("/queue-add"):
                self.search_track = self.helper.parse_command(event.value)
                self.queue_options = await fetch_tracks_list(self.search_track)
                if self.queue_options:
                    layout_widget.update_dashboard(self.queue_options, "Type track no. to be added to queue :-")
                    self.update_input()
                    self.select_from_queue = True

            if event.value.isdigit() and self.select_from_queue:
                self.should_play_queue = True
                self.track_to_be_added_to_queue = self.queue_options[int(event.value)-1]
                self.queue[self.search_track] = self.track_to_be_added_to_queue
                self.update_input()
                self.search_track=""

            if event.value.startswith("/show-queue"):
                tracks = self.queue.values()
                data = "\n".join(tracks)
                layout_widget.update_dashboard(data, "Current Queue :-")
                self.update_input()

            if event.value.startswith("/pause"):
                self.action_pause()

            if event.value.startswith("/resume"):
                self.action_resume()
            


    def action_pause(self):
        """Pause the player"""
        layout_widget = self.query_one(RichLayout)
        self.player.pause()
        layout_widget.update_playing_status()


    def action_resume(self):
        """Resume the player"""
        layout_widget = self.query_one(RichLayout)
        if not self.player.is_playing:
            self.player.resume()
            layout_widget.update_playing_status()

    def action_volume_up(self):
        """Increase the volume by 5 levels"""
        current_volume = self.player.get_volume()
        self.player.set_volume(current_volume+5)
        layout_widget = self.query_one(RichLayout)
        layout_widget.update_volume(self.player.get_volume())

    def action_volume_down(self):
        """Decrease the volume by 5 levels"""
        current_volume = self.player.get_volume()
        self.player.set_volume(current_volume-5)
        layout_widget = self.query_one(RichLayout)
        layout_widget.update_volume(self.player.get_volume())

    def handle_play(self, track_name: str):
        """Function to handle the track playback"""
        layout_widget = self.query_one(RichLayout)
        url = get_audio_url(track_name+" official audio")
        self.track_url = url
        self.player.set_volume(50)
        self.player.play(url)
        add_track_to_recents(helper.Format.clean_hashtag(track_name))
        layout_widget.update_track(track_name)
        self.current_track_duration = TrackInfo.get_audio_duration(url)
        layout_widget.update_total_track_time(TrackInfo.get_audio_duration(url))
        color_ind = random.randint(0,9)
        layout_widget.update_color(color_ind)

    def update_input(self) -> None:
        """Function to reset the data in input widget once user enters his input"""
        input_widget = self.query_one(Input)
        input_widget.placeholder = ""
        input_widget.value = ""
    
    def update_track_progress(self) -> None:
        """Function to update track progress"""
        layout_widget = self.query_one(RichLayout)
        layout_widget.update_music_progress(TrackInfo.get_current_time(self.player), int(TrackInfo.get_progress(self.player)))
        if self.current_track_duration == TrackInfo.get_current_time(self.player):
            if self.queue:
                keys = list(self.queue.keys())
                tracks = list(self.queue.values())
                key = keys[0]
                track = tracks[0]
                del self.queue[key]
                self.handle_play(track)

  
    