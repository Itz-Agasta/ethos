from .textual_app import TextualApp

class UI:
    """UI class for drawing the ethos UI"""

    def __init__(self):
        self.app = TextualApp()

    def draw_ui(self):
        """Function to draw the UI"""
        self.app.run()
