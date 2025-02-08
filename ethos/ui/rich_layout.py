from textual.widget import Widget
from textual.reactive import reactive
from rich.layout import Layout
from rich.text import Text
from rich.padding import Padding
from rich.align import Align
from rich.panel import Panel
from rich.progress_bar import ProgressBar
from typing import Optional
from ethos.ui.utils import assets, square_drawer
from ethos.tools import helper
from datetime import datetime


class Clock:
    """Renders the time in the center of the screen."""

    def __rich__(self) -> Text:
        return Text(datetime.now().ctime(), style="bold magenta", justify="center")


class RichLayout(Widget):
    """Rich Widget for ethos UI"""

    ASSETS = assets.UIAssets()
    layout = reactive(Layout)
    current_song = reactive("")
    current_artist = reactive("")
    is_player_playing = reactive(False)
    logs = reactive("")
    queue = reactive("")
    dashboard_title = reactive("")
    dashboard_data = reactive("")
    volume = reactive(50)
    colors_ = ['bright_magenta', 'green3', 'blue', 'cyan1', 'bright_red', 'bright_white', 'dark_slate_gray2', 'orange3', 'yellow1', 'grey62', 'turquoise2']
    color = reactive("")
    random_int = reactive(0)
    style = reactive("")
    square:Text = square_drawer.draw_square(4)
    music_progress:str = reactive("")
    music_progress_int = 0
    total_track_time:str = reactive("")
    progress_bar = ProgressBar(total=100, completed=0)
    log_data = reactive("")


    def on_mount(self) -> None:
        """Initialize the layout when the widget is mounted"""

        self.layout = Layout()
        self.layout.split(
            Layout(name="header", size=1),
            Layout(ratio=1, name="main"),
            Layout(size=7, name="player"),
        )
        self.layout.box = False

        self.layout["main"].split_row(Layout(name="side", ratio=3), Layout(name="cat", ratio=2))
        self.layout["side"].split(Layout(name="branding", size=7), Layout(name="dashboard"))
        self.layout["player"].split_row(Layout(name="song_info", ratio=3), Layout(name="buttons", ratio=3), Layout(name="music-progress", ratio=3), Layout(name="volume", ratio=1))
        self.layout["music-progress"].split_row(Layout(name="music-progress-bar", ratio=3), Layout(name="music-progress-float", ratio=2))
        self.layout["song_info"].split_row(Layout(name="square", ratio=1), Layout(name="song-metadata", ratio=3))
        self.layout["dashboard"].split(Layout(name="dashboard-title", size=3), Layout(name="dashboard-data"), Layout(name="log", size=2))
    

    def update_layout(self):
        """Make the layout for app dashboard"""

        
        self.layout["cat"].update(
            Align.center(
                Text(
                    self.ASSETS.CAT_SYMBOL,
                    style="bold magenta",
                    justify="default"
                ),
                vertical="middle",
            )
        )

        self.layout["branding"].update(
            Align.center(
                Text(
                    self.ASSETS.BRANDING,
                    style="bold magenta",
                    justify="center"
                ),
                vertical="middle",
            )
        )

        self.layout["header"].update(Clock())
        self.layout["buttons"].update(
                Align.center(
                    Text(self.ASSETS.BUTTON_SYMBOLS["playing"] if self.is_player_playing else self.ASSETS.BUTTON_SYMBOLS["paused"],
                    style="bold green",
                    justify="center"),
                    vertical="middle"
                )
        )
        self.layout["volume"].update(
            Align.center(
                Text(f"Volume: {self.volume}",
                style="bold green",
                justify="center"),
                vertical="middle"
            )
        )
        self.layout["square"].update(
                Align.right(
                    Text(f"{self.square}",
                         style=self.style),
                    vertical="middle"
                ),
        )
        self.layout["song-metadata"].update(
                Align.left(
                    Padding(f"{self.current_song}\n{self.current_artist}",
                            (1,1),
                            style=f"bold {self.color}",
                         ),
                         vertical="middle"
                )
        )
        self.layout["dashboard-title"].update(
            Panel(
                Align.center(
                    Text(self.dashboard_title,
                         style="reverse bold green",
                         justify="default"),
                         vertical="middle"
                )
            )
        )
        self.layout["dashboard-data"].update(
            Panel(
                Text(
                    self.dashboard_data,
                    justify="default"
                ),
            )
        )
        self.layout["music-progress-bar"].update(
            Align.center(self.progress_bar,
                         vertical="middle")
            )
        self.layout["music-progress-float"].update(
            Align.center(
                Text(f"{self.music_progress if not self.music_progress.startswith('-') else '0.0'} / {self.total_track_time or '0.0'}",
                     style="bold green",
                     justify="default"),
                     vertical="middle"
            )
        )
        self.layout["log"].update(
            Align.center(
                Text(self.log_data,
                    style="bold green",
                    justify="center"),
                    vertical="middle"
            )
        )
        
    def update_track(self, track_name: str) -> None:
        """Update the current playing song"""
        self.current_song, self.current_artist = helper.Format.extract_song_and_artist(track_name)
        self.is_player_playing = True
        self.refresh()
    

    def update_playing_status(self) -> None:
        """Update playing status of the player to render the controller buttons"""
        if self.is_player_playing:
            self.is_player_playing = False
        else:
            self.is_player_playing = True
        self.refresh()


    def update_color(self, color_ind: int) -> None:
        """Update the color for track and artist"""
        self.random_int = color_ind
        self.color = self.colors_[color_ind]
        self.style = f"reverse {self.color}"
        self.refresh()


    def update_dashboard(self, data: any, title: Optional[str]) -> None:
        """Dynamically update dashboard data based on user interactions"""
        if type(data) == list:
            self.dashboard_data = "\n".join(data) + "\nType track number to play"
        if type(data) == str:
            self.dashboard_data = data
        self.dashboard_title = title
        self.refresh()


    def update_volume(self, volume: int) -> None:
        self.volume = volume
        self.refresh()
                    
    def update_music_progress(self, progress:str, progress_int: int) -> None:
        self.music_progress = progress
        self.music_progress_int = progress_int
        self.progress_bar = ProgressBar(total=100, completed=self.music_progress_int)
        self.refresh()
    
    def update_total_track_time(self, track_time: str) -> None:
        """Update total track time when a new track is played"""
        self.total_track_time = track_time
        self.refresh()

    def update_log(self, log_data: str) -> None:
        self.log_data = log_data
        self.refresh()

    def show_commands(self) -> None:
        commands = self.ASSETS.COMMANDS
        self.dashboard_data = ""
        self.dashboard_title = "List of valid commands :"
        for key, value in commands.items():
            self.dashboard_data = self.dashboard_data + "\n" + f"{key} : {value}"
        self.refresh()

    def render(self) -> Layout:
        """Render the widget"""

        self.update_layout()
        return self.layout