import os

def resolve_playlists(playlist_path):
    """Function to check if any playlist exist"""
    return os.listdir(playlist_path)

def is_recents(recent_file_path):
    """Function to check if any recent file exists"""
    return os.path.exists(recent_file_path)

def resolve_recents(recents_path):
    """Function to resolve last 5 played songs"""
    if is_recents(recents_path):
        import json
        return json.loads(open(recents_path).read())