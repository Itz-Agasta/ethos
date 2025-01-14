from yt_dlp import YoutubeDL

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
