import os
from dotenv import load_dotenv
from pathlib import Path
from typing import Optional

load_dotenv()

class ConfigManager:
    """
    Manages the configuration for the application, including methods
    for retrieving, updating, and deleting the music folder path.

    Configuration can be sourced from:
      - `MUSIC_FOLDER` environment variable (`.env` file).
      - A configuration file (`~/.ethos/ethosrc`) in the user home directory.
    """
    def __init__(self):
        self.env_music_folder = os.getenv("MUSIC_FOLDER")
        self.config_dir = Path.home() / ".ethos"
        self.config_file = self.config_dir / "ethosrc"

    def get_music_folder_from_env(self) -> Optional[Path]:
        if self.env_music_folder:
            return Path(self.env_music_folder)
        return None

    def get_music_folder_from_rc(self) -> Optional[Path]:
        if self.config_file.exists():
            with open(self.config_file, "r") as file:
                for line in file:
                    if line.startswith("MUSIC_FOLDER="):
                        music_folder = line.split("=", 1)[1].strip()
                        if music_folder:
                            return Path(music_folder)
        return None

    def prompt_user_for_music_folder(self) -> Path:
        """
        Prompt the user to input their music folder path and save it to the configuration file.

        :return: A Path object representing the user-specified music folder.
        """
        music_folder = input("Please enter the path to your music folder: ").strip()
        self.config_dir.mkdir(exist_ok=True)
        with open(self.config_file, "w") as file:
            file.write(f"MUSIC_FOLDER={music_folder}\n")
        return Path(music_folder)

    def fetch_config(self) -> Optional[Path]:   #TODO:  use this function to retrieve the spotify api-key also.
        """
        Primary method to retrieve the music folder path in the following order of precedence:
          1. `MUSIC_FOLDER` from the .env file, if set.
          2. Configuration file (`~/.ethos/ethosrc`) in the user home directory, if it exists.
          3. User input (if the above methods fail).

        :return: A Path object representing the music folder if found, otherwise None.
        """
        music_folder = self.get_music_folder_from_env() 
        if music_folder:
            return music_folder

        music_folder = self.get_music_folder_from_rc() 
        if music_folder:
            return music_folder

        return self.prompt_user_for_music_folder() 

    def rewrite_config(self) -> Path:
        """Overwrite the existing configuration with a new music folder path provided by the user."""
        return self.prompt_user_for_music_folder()

    def delete_config(self) -> None:
        """ Delete the configuration file if it exists."""
        if self.config_file.exists():
            self.config_file.unlink()

def get_music_folder() -> Optional[Path]:
    """
    Retrieves the music folder path using the `ConfigManager`.

    :return: A Path object for the music folder, or None if unavailable.
    """
    config_manager = ConfigManager()
    return config_manager.fetch_config()


# FIXME: Handle the case where Windows users accidentally use a single backslash
# in the path (escape character issues). Implement sanitization for such paths.
