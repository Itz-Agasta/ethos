from yt_dlp import YoutubeDL
import os
import base64
from dotenv import load_dotenv, find_dotenv
from time import time
import httpx
from pathlib import Path
from tools.helper import Format
import json

load_dotenv(dotenv_path=find_dotenv(filename=".env"))

class Search:
    """Utility class for searching track metadata and url from external APIs"""


    @staticmethod
    def get_audio_url(query):
        """
        Fetches the audio URL for a given search query using YoutubeDL. The function
        utilizes specific configuration options to return the best available audio
        source while ensuring no playlists are processed and only the top search
        result is fetched. It does not download the file, only extracts the URL for
        the audio stream.

        :param query: A string representing the search query used to find the audio
            content on YouTube. It can include keywords or phrases to search for.
        :type query: str

        :return: The URL string of the best audio stream available based on the given
            search query.
        :rtype: str
        """
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'default_search': 'ytsearch1',
        }

        with YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(query, download=False)
            if 'entries' in result:
                result = result['entries'][0]
            return result['url']



    @staticmethod
    async def get_spotify_token(client_id="e904c35efb014b76bd8999a211e9b1e1", client_secret="af18ccf7adae4ea7b37ca635c4225928"):
        """
        Fetches authorization token from spotify
        
        Args: client_id(str), client_secret(str)
        
        return: spotify authorization token
        """

        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": "Basic " + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
        }
        data = {"grant_type": "client_credentials"}
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, data=data)
            response_data = response.json()

        if response.status_code != 200:
            raise Exception(f"Failed to get token: {response_data}")
        
        return response_data["access_token"]


    @staticmethod
    async def search_tracks_from_spotify(track_name, token):
        """
        Searches for a track in spotify and returns first 10 entries of search results
        
        Args: track_name(str), token(str)
        
        return: tracks(list)
        """

        url = "https://api.spotify.com/v1/search"
        headers = {
            "Authorization": f"Bearer {token}"
        }
        params = {
            "q": track_name,
            "type": "track",
            "limit": 10  
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params=params)
            response_data = response.json()

        if response.status_code != 200:
            raise Exception(f"Failed to fetch tracks: {response_data}")
        
        return response_data["tracks"]["items"]


    @staticmethod
    async def fetch_tracks_list(track_name: str) -> list:
        """
        Returns a list of track name and artist name from tracks info

        Args: track_name(str)

        return: list
        """

        fetched_tracks = []
        try:
            
            start_time = time()
            token = await Search.get_spotify_token()
            tracks = await Search.search_tracks_from_spotify(track_name, token)
            if tracks:
                print(f"\nTracks found for '{track_name}':")
                for idx, track in enumerate(tracks, start=1):
                    track_info = f"{idx}. {track['name']} by {', '.join(artist['name'] for artist in track['artists'])}"
                    #print(track_info)
                    fetched_tracks.append(track_info.strip())
            else:
                print(f"No tracks found for '{track_name}'.")
        
        except Exception as e:
            print(f"Error: {e}")

        finally:
            end_time = time()
            print("Time taken to get metadata = %.2f" % (end_time - start_time))
            return fetched_tracks
        

    @staticmethod
    async def search_artist_id_from_spotify(artist_name, token):
        """Search for an artist on Spotify and return their ID."""
        url = f"https://api.spotify.com/v1/search?q={artist_name}&type=artist&limit=1"
        headers = {"Authorization": f"Bearer {token}"}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data["artists"]["items"]:
                return data["artists"]["items"][0]["id"]
            else:
                raise Exception("No artist found!")
        else:
            raise Exception(f"Failed to search artist: {response.json()}")

        
    @staticmethod
    async def search_song_id_from_spotify(song_name, token):
        """Search for a song on Spotify."""
        url = f"https://api.spotify.com/v1/search?q={song_name}&type=track&limit=1"
        headers = {"Authorization": f"Bearer {token}"}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data["tracks"]["items"]:
                    return data["tracks"]["items"][0]["id"]
                else:
                    raise Exception("No song found!")
            else:
                raise Exception(f"Failed to search song: {response.json()}")


    @staticmethod
    async def fetch_top_tracks(artist_id, token, market="US"):
        """Fetch top tracks of an artist."""
        url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market={market}"
        headers = {"Authorization": f"Bearer {token}"}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                tracks = []
                for track in data["tracks"]:
                    tracks.append({
                        "name": track["name"],
                        "artist": track["artists"][0]["name"]
                    })
                print(tracks)
                return tracks
            else:
                raise Exception(f"Failed to fetch top tracks: {response.json()}")
            

    @staticmethod
    async def get_track_image(song_id, token):
        """Fetch the track's album image URL using the Spotify API."""
        url = f"https://api.spotify.com/v1/tracks/{song_id}"
        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response_data = response.json()
            
            if response.status_code == 200:
                album_images = response_data["album"]["images"]
                if album_images:
                    # Return the highest resolution image (usually the first one)
                    return album_images[0]["url"]
                else:
                    return "No album images found."
            else:
                raise Exception(f"Failed to get track data: {response_data}")
    

class UserFiles:
    """Utility class for performing operations related to userfiles like recents and playlists"""

    @staticmethod
    def fetch_recents() -> list[str]:
        """Fetches the recent tracks and returns it in a list"""

        recents_file = Path.home() / ".ethos" / "userfiles" / "recents.txt"
        recents = []
        try:
            if os.path.exists(recents_file):
                with open(recents_file, 'r') as file:
                    for line in file:
                        recents.append(line.strip())
        except:
            return
        return recents


    @staticmethod
    def add_track_to_recents(track: str):
        """Writes a track to the recents file, keeping only the last 10 entries."""
        recents_dir = Path.home() / ".ethos" / "userfiles"
        recents_file = recents_dir / "recents.txt"
        
        recents_dir.mkdir(parents=True, exist_ok=True)

        lines = []
        if recents_file.exists():
            try:
                with open(recents_file, "r") as file:
                    lines = file.readlines()
            except Exception as e:
                return f"Error reading recents file: {e}"

        track = track.strip()
        removed_track = track+"\n"
        if track+"\n" in lines:
            lines.remove(removed_track)
        lines.insert(0, track + "\n")

        lines = lines[:10]

        try:
            with open(recents_file, "w") as file:
                file.writelines(lines)
        except Exception as e:
            return f"Error writing to recents file: {e}"


    @staticmethod
    def fetch_tracks_from_playlist(playlist_name: str) -> list[str]:
            """
            Function to fetch all songs from a playlist.json file.

            Args:
            - playlist_name (str): name of a playlist

            Returns:
            - list: List of all songs in a particular playlist
            """
            playlist_file = Path.home() / ".ethos" / "userfiles" / "playlists" / f"{playlist_name}.json"
            tracks = []
            try:
                if os.path.exists(playlist_file):
                    with open(playlist_file, 'r') as playlist:
                        tracks_json = json.load(playlist)
                        for track in tracks_json:
                            name = track["name"]
                            artist = track["artist"]
                            tracks.append(f"{name} by {artist}")
            except:
                pass
                return 
            return tracks


    @staticmethod
    def add_track_to_playlist(playlist_name: str, track_name: str) -> None:
        """
        Function to add tracks to a playlist
        
        Args:
        - playlist_name (str): name of a playlist
        """
        playlist_dir = Path.home() / ".ethos" / "userfiles" / "playlists"
        playlist_file = playlist_dir / f"{playlist_name}.json"

        playlist_dir.mkdir(parents=True, exist_ok=True)
        tracks = []
        track, artist = Format.extract_song_and_artist(track_name)
        tracks.append({"name": track, "artist": artist})
        try:
            if os.path.exists(playlist_file):
                with open(playlist_file, 'r') as playlist:
                    tracks_json = json.load(playlist)
                    for track in tracks_json:
                        tracks.append(track)

            with open(playlist_file, 'w') as file:
                json.dump(tracks, file, indent=4)
        except:
            pass


    @staticmethod
    def fetch_playlists() -> list[str]:
        """
        Function to fetch all playlists from playlist path
        """
        try:
            playlists = []
            playlist_dir = Path.home() / ".ethos" / "userfiles" / "playlists"
            files = os.listdir(playlist_dir)
            for f in files:
                playlist = os.path.basename(playlist_dir / f).split('.')[0]
                if playlist:
                    playlists.append(playlist)

            return playlists
        except:
            pass
            return