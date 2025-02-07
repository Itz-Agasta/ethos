import os
import json
from pathlib import Path
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

class SpotifyImporter:
    """
    Class for interacting with Spotify's API to fetch and manage playlist data locally.

    This class authenticates a user, fetches playlists, saves their tracks as JSON files,
    and provides methods to refresh playlist data.
    """
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.spotify = self._authenticate()
        self.config_dir = Path.home() / ".ethos"

    def _authenticate(self) -> Spotify:
        scope = "user-library-read playlist-read-private"
        auth_manager = SpotifyOAuth(client_id=self.client_id, client_secret=self.client_secret, redirect_uri=self.redirect_uri, scope=scope)
        return Spotify(auth_manager=auth_manager)

    def fetch_playlists(self):
        # Retrieve the playlists for the authenticated Spotify user
        playlists = self.spotify.current_user_playlists()
        return playlists['items']

    def save_playlist_to_json(self, playlist_id: str, playlist_name: str):
        # Fetch all tracks from the playlist
        results = self.spotify.playlist_tracks(playlist_id)
        tracks = results['items']

        songs = []  # Create a list of songs with their name and artist's name
        for item in tracks:
            track = item['track']
            song_info = {
                'name': track['name'],
                'artist': track['artists'][0]['name']
            }
            songs.append(song_info)

        self.config_dir.mkdir(exist_ok=True)
        playlist_file = self.config_dir / f"{playlist_name}.json"
        with open(playlist_file, 'w') as f:
            json.dump(songs, f, indent=4)

    def refresh_all_playlists(self):
        # Refreshes all playlists by fetching the latest data and saving it to JSON files.
        playlists = self.fetch_playlists()
        for playlist in playlists:
            self.refresh_playlist(playlist['id'], playlist['name'])

    def refresh_playlist(self, playlist_id: str, playlist_name: str):
        """
        Refreshes a specific playlist by updating the JSON file with new data.
        If the file already exists, it adds any new songs not already saved.

        Args:
            playlist_id (str): The unique ID of the playlist.
            playlist_name (str): The name of the playlist for the JSON file.
        """
        results = self.spotify.playlist_tracks(playlist_id)
        tracks = results['items']

        # Create a list of the latest songs
        new_songs = []
        for item in tracks:
            track = item['track']
            song_info = {
                'name': track['name'],
                'artist': track['artists'][0]['name']
            }
            new_songs.append(song_info)

        # Where the playlist JSON file will be stored
        playlist_file = self.config_dir / f"{playlist_name}.json"
        if playlist_file.exists(): # If the file exists, load the current songs and only append new ones
            with open(playlist_file, 'r') as f: 
                existing_songs = json.load(f)
            existing_song_names = {song['name'] for song in existing_songs}
            for song in new_songs:
                if song['name'] not in existing_song_names:
                    existing_songs.append(song)
            with open(playlist_file, 'w') as f: # Save the updated playlist data 
                json.dump(existing_songs, f, indent=4)
        else:
            with open(playlist_file, 'w') as f: # If the file exists, load the current songs and only append new ones
                json.dump(new_songs, f, indent=4)

       # print(f"Playlist '{playlist_name}' has been refreshed.")



####################
## Temporary test ##
###################
if __name__ == "__main__":
    client_id = os.getenv("SPOTIFY_CLIENT_ID")
    client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    redirect_uri = os.getenv("REDIRECT_URI") or "http://localhost:3000/"

    importer = SpotifyImporter(client_id, client_secret, redirect_uri)
    playlists = importer.fetch_playlists()

    print("Available Playlists:")
    for idx, playlist in enumerate(playlists):
        print(f"{idx + 1}. {playlist['name']}")

    choice = int(input("Select a playlist to import: ")) - 1
    selected_playlist = playlists[choice]
    importer.save_playlist_to_json(selected_playlist['id'], selected_playlist['name'])

    print(f"Playlist '{selected_playlist['name']}' has been saved.")
    
    # importer.refresh_all_playlists() # Refresh all playlists
