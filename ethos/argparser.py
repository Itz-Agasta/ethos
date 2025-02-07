import argparse
from ethos.utils import get_audio_url, fetch_tracks_list
from ethos.player import MusicPlayer, TrackInfo
from ethos.tools import helper
from rich.console import Console
import asyncio
import time

class ArgumentParser():
    """Argument Parser class for ethos cli"""

    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Ethos CLI App")
        self.console = Console(color_system='256')
        self.player = MusicPlayer()
    
    def start(self, args) -> None:
        """Start the player"""
        self.console.print("[magenta]Starting ethos cli...")

    def stop(self, args) -> None:
        """Stop the player"""
        self.console.print("[magenta]Stopping ethos cli...")

    def status(self, args) -> None:
        """Sets the status of the player"""
        self.console.print("[magenta]Status ethos cli...")
    
    async def play(self, args) -> None:
        """Plays a track provided by the user"""

        track = args.track if args.track else str(input("Enter track name to play :"))
        self.console.print(f"[cyan]Fetching track: {track}")
        tracks_list = await fetch_tracks_list(track)
        track_no = 0
        if not args.track_no:
            if tracks_list:
                self.console.print("Search results :")
                self.console.print("\n".join(tracks_list))
                track_no = int(input("Enter track number :"))
        track_name = helper.Format.clean_hashtag(tracks_list[track_no-1])
        track_url = get_audio_url(track_name+"official music video")

        if not track_url:
            self.console.print(f"[red]Could not fetch URL for {track_name}")
            return

        volume = args.volume if args.volume else 50
        self.console.print("[deep pink]Playing at default volume: 50")
        self.player.set_volume(volume)
        self.player.play(track_url)
        
        self.console.print(f"[deep pink]Playing {track_name}")
        track_length = TrackInfo.get_audio_duration_int(track_url)
        while TrackInfo.get_current_time_int(self.player) < track_length:
            time.sleep(1)
        if TrackInfo.get_current_time_int(self.player) == track_length:
            return

    async def listen(self) -> None:
        """Listens to commands from cli"""
        self.subparsers = self.parser.add_subparsers(dest="command", help="Available commands:")

        self.start_parser = self.subparsers.add_parser("start", help="Start the app")
        self.start_parser.set_defaults(func=self.start)

        self.stop_parser = self.subparsers.add_parser("stop", help="Stop the parser")
        self.stop_parser.set_defaults(func=self.stop)

        self.status_parser = self.subparsers.add_parser("status", help="Check status")
        self.status_parser.set_defaults(func=self.status)

        self.play_parser = self.subparsers.add_parser("play", help="play a track")
        self.play_parser.add_argument("track", type=str, nargs="?", help="name of the track you want to play")
        self.play_parser.add_argument("track_no", type=int, nargs="?", help="track no. of track to be played from search results")
        self.play_parser.add_argument("volume", type=int, nargs="?", help="volume of the player")
        self.play_parser.set_defaults(func=self.play)

        self.args = self.parser.parse_args()

        if hasattr(self.args, "func"):
            await self.args.func(self.args)

        else:
            self.parser.print_help()


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    asyncio.run(arg_parser.listen())

