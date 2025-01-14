import os
from dotenv import load_dotenv
from pathlib import Path
from typing import Optional

load_dotenv()

def get_music_folder() -> Optional[Path]:
    """
    Retrieves the path of the music folder from the environment variable.

    This function checks for the `MUSIC_FOLDER` environment variable and, if it
    exists, returns its value as a `Path` object. If the environment variable is
    not set, the function returns `None`.

    :return: A `Path` object representing the music folder if the environment
        variable `MUSIC_FOLDER` is set, otherwise `None`.
    :rtype: Optional[Path]
    """
    music_folder = os.getenv("MUSIC_FOLDER")
    if music_folder:
        return Path(music_folder)
    return None

# TODO: Get and store the user music folder location 1 time only when the user first runs the program.
# For development, we will use .env file to store the music folder location. 