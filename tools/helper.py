class formate:
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