from yt_dlp import YoutubeDL
import os
from shazamio import Shazam
# from spotipy import Spotify
# from spotipy.oauth2 import SpotifyClientCredentials

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
"""
def get_spotify_client():
    client_id = os.getenv("SPOTIPY_CLIENT_ID")
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
    return Spotify(client_credentials_manager=SpotifyClientCredentials(client_id, client_secret))

async def get_song_metadata(query):  # Took 10 sec approx
    
    Downloads the title of the requested song using yt-dlp, and uses Spotipy to get the song name in "song - artist" format.

    :param query: A string representing the search query used to find the audio content.
    :type query: str

    :return: A string in the format "song - artist name".
    :rtype: str
    
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
        title = result['title']

    spotify = get_spotify_client()
    search_result = spotify.search(q=title, type='track', limit=1)
    if search_result['tracks']['items']:
        track = search_result['tracks']['items'][0]
        song = track['name']
        artist = track['artists'][0]['name']
        metadata = f"{song} - {artist}"
    else:
        metadata = "Unknown - Unknown"

    return metadata
"""

async def get_song_metadata(query): # Took 12 sec approx in async environment
    """
    Downloads a short audio snippet using yt-dlp, uses Shazam to recognize the song,
    and deletes the snippet once the metadata is retrieved.

    :param query: A string representing the search query used to find the audio content.
    :type query: str

    :return: A string in the format "song - artist name".
    :rtype: str
    """
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'default_search': 'ytsearch1',
        'outtmpl': 'snippet.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'postprocessor_args': [
            '-t', '5',  # Download only the first 5 seconds
        ],
    }

    with YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(query, download=True)
        if 'entries' in result:
            result = result['entries'][0]
        snippet_path = 'snippet.mp3'

    shazam = Shazam()
    out = await shazam.recognize_song(snippet_path)

    if out['matches']:
        song = out['track']['title']
        artist = out['track']['subtitle']
        metadata = f"{song} - {artist}"
    else:
        metadata = "Unknown - Unknown"

    os.remove(snippet_path)
    return metadata


# Normally took 4 sec for a online playback and 2 sec for a local playback.
