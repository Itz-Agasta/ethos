from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Input, Button, Label, ListView, ListItem, ProgressBar
from textual.containers import Horizontal, Vertical, Container
from textual.reactive import var
from textual.timer import Timer
from helper_functions import resolve_playlists, resolve_recents

class EthosMusicCLI(App):
    """UI for ethos music player"""

    CSS_PATH = "./ui.tcss"
    progress_time: Timer
    """Timer for music progress"""


    """Defining all reactive elements"""
    search = var("")
    queue = var([])
    now_playing = var("")
    time_stamp = var(0)
    player_paused = var(True)

    playlist_path = "../userfiles/playlists"
    recents_path = "../userfiles/recents.json"
    playlists = resolve_playlists(playlist_path)
    recents = var(resolve_recents(recents_path))
    
    def compose(self) -> ComposeResult:

        """
        DOM Structure:
        Horizontal
            Vertical
                Hero Section
                Playlists
            Vertical
                Search
                Recents
                Player
        """
        
        yield Header()
        yield Footer()

        branding = '''   ▄████████     ███        ▄█    █▄     ▄██████▄     ▄████████ 
  ███    ███ ▀█████████▄   ███    ███   ███    ███   ███    ███ 
  ███    █▀     ▀███▀▀██   ███    ███   ███    ███   ███    █▀  
 ▄███▄▄▄         ███   ▀  ▄███▄▄▄▄███▄▄ ███    ███   ███        
▀▀███▀▀▀         ███     ▀▀███▀▀▀▀███▀  ███    ███ ▀███████████ 
  ███    █▄      ███       ███    ███   ███    ███          ███ 
  ███    ███     ███       ███    ███   ███    ███    ▄█    ███ 
  ██████████    ▄████▀     ███    █▀     ▀██████▀   ▄████████▀  
                                                                '''
        
        subtitle = '''music-cli for cool folks'''
        guitar = """                          ,     
                      ,   |     
   _,,._              |  0'     
 ,'     `.__,--.     0'         
/   .--.        |           ,,, 
| [=========|==|==|=|==|=|==___]
\   "--"  __    |           ''' 
 `._   _,'  `--'                
    ""'     ,   ,0     ,        
hjm         |)  |)   ,'|        
  ____     0'   '   | 0'        
  |  |             0'           
 0' 0'"""
        #art - Guitar by Harry Mason

        player_symbols_playing = """                                                            
    :*%+   =#%.   .+*= :**:    *%+.  :%#-         --. .-:   
  =%@@@#:*@@@@:   -@@@ *@@*    @@@@#-=@@@@+.    .@@@@%@@@@. 
:@@@@@@@@@@@@@:   -@@@ *@@*    @@@@@@@@@@@@@+   .@@@@@@@@@  
 =%@@@@%*@@@@@:   -@@@ *@@*    @@@@@%#@@@@@*.     +@@@@@+   
   :*@@#  =%@@:   -@@@ *@@*    @@@+. =@@#-          =#=     
      -.    ::     -=: .==.    .:     -.                    
"""
        player_symbols_paused = """                 .-.                                        
    :*%+   =#%.  %@@%+:        *%+.  :%#-         --. .-:   
  =%@@@#:*@@@@:  %@@@@@@*-     @@@@#-=@@@@+.    .@@@@%@@@@. 
:@@@@@@@@@@@@@:  %@@@@@@@@@#   @@@@@@@@@@@@@+   .@@@@@@@@@  
 =%@@@@%*@@@@@:  %@@@@@@@%+:   @@@@@%#@@@@@*.     +@@@@@+   
   :*@@#  =%@@:  %@@@@*-.      @@@+. =@@#-          =#=     
      -.    ::   +#+:          .:     -.                    
"""

        yield Horizontal(
            Vertical(
                Static(branding, classes="title"),
                Static(subtitle, classes="sub_title"),
                Container(
                    Static("[@click='app.bell']Your playlists[/]", classes="playlist_title"),
                    ListView(classes="playlist_list") if self.playlists else Static("No playlists available", classes="playlist_list"),
                    Static("[@click='app.create_playlist']Create Playlist [0][/]", classes="playlist_button"),
                )
            ),
            Vertical(
                Input(placeholder="Search music\t[s]", type="text", value=self.search, classes="search"),
                Container(
                    Static("Recents", classes="recents_title"),
                    ListView(classes="recents_list"),
                    id="recents"
                ),
                Container(
                    Static(f"Listening {self.now_playing}", classes="player_title"),
                    ProgressBar(),
                    Static(player_symbols_paused if self.player_paused else player_symbols_playing),
                    id="player"
                )
            ),
        )

    def on_mount(self) -> None:
        self.title = "ethos"
        self.sub_title = "music cli"
        self.screen.styles.background = "black"
        self.screen.styles.border = ("heavy", "green")

        """Define the ui for playlists"""
        playlists_list = self.query_one('.playlist_list', ListView)
        try:
            if self.playlists:
                for playlist in self.playlists:
                    """Extract playlist name from path"""
                    import os
                    playlist_name = os.path.splitext(os.path.basename(playlist))[0]
                    playlists_list.append(ListItem(Label(f"[@click='app.show_playlist({playlist})']{playlist_name}[/]")))
            
        except:
            playlists_list.append(ListItem(Label("Playlists not available")))
        
        """Define the ui for recents"""
        list_view = self.query_one('.recents_list', ListView)
        try:
            if self.recents:
                self.recents_generator = ((entry['song'], entry['artist']) for entry in self.recents)
                for song, artist in self.recents_generator:
                    """Generate the search term from recents list"""
                    s = "song" + "-" + "artist"
                    list_view.append(ListItem(Label(f"[@click='app.play_song({s})']{song} - {artist}[/]")))
            else:
                list_view.append(ListItem(Label("You have not played any song recently")))
        except:
            list_view.append(ListItem(Label("Recents not available")))

        self.progress_time = self.set_interval(1 / 10, self.make_progress, pause=True)

    def make_progress(self) -> None:
        """Update the music progress"""
        self.query_one(ProgressBar).advance(1)

    def action_start(self) -> None:
        """Start the music"""
        self.query_one(ProgressBar).update(total=100)
        self.progress_time.resume()



if __name__ == "__main__":
    app = EthosMusicCLI()
    app.run()
