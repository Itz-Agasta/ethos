class Format:
    @staticmethod
    def seconds_to_min_sec(seconds: int) -> str:
        """
        Convert seconds to a string in the format min:sec.

        Args:
        - seconds (int): The duration in seconds.

        Returns:
        - str: The duration in min:sec format.
        """
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{minutes}:{remaining_seconds:02}"

    
    @staticmethod
    def extract_item_number(entry: str) -> int:
        """Regex method to extract the item number from tracks list"""
        import re
        match = re.match(r'^(\d+)\.', entry)
        if match:
            return int(match.group(1))
        return None
    
    @staticmethod
    def parse_command(command: str):
        """
        Parses commands like '/play after hours' and '/volume 50' to extract values.
    
        Args:
            command (str): The command string to parse
        
        Returns:
            str or int: The extracted value after the command
                - For /play commands: returns the song name as string
                - For /volume commands: returns the volume level as integer
        """
        parts = command.split(maxsplit=1)
    
        if len(parts) != 2:
            raise ValueError("Invalid command format")
        
        command_type, value = parts
    
        if command_type == '/play' or command_type == '/queue-add' or command_type == '/queue-remove' or command_type == "/vp":
            return value
        elif command_type == '/volume' or command_type == '/qp':
            try:
                return int(value)
            except ValueError:
                raise ValueError("Volume must be a number")
        elif command_type == '/ap':
            try:
                parts = value.split(maxsplit=1)
                playlist_name, track_name = parts
                return playlist_name, track_name
            except:
                pass
        
        
    
    @staticmethod
    def extract_song_and_artist(text: str) -> tuple[str, str]:
        """
        Extracts the song name and artist name from the text in the following formats:
        1. <Song No.>.<Song name> by <Artist Name>
        2. <Song name> by <Artist Name>
        
        Args:
            text (str): The input text.
            
        Returns:
            tuple[str, str]: A tuple containing the song name and artist name.
            
        Raises:
            ValueError: If the input text is not in the expected format.
        """
        import re
        
        pattern_with_number = r'^\d+\.\s*(.+?)\s+by\s+(.+)$'
        pattern_without_number = r'^(.+?)\s+by\s+(.+)$'
        
        match = re.match(pattern_with_number, text) or re.match(pattern_without_number, text)
        
        if match:
            song_name = match.group(1)
            artist_name = match.group(2)
            return song_name, artist_name
        else:
            raise ValueError("Input text is not in the expected format.")


    @staticmethod
    def clean_hashtag(text: str) -> str:
        """Removes the entry number from the track name"""
        import re
        return re.sub(r'^(\d+\. )', r'', text)
