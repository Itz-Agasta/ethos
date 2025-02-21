########################
# Entry point of Ethos #
########################

import os
import sys
from ethos.ui import ui

def main():
    """Main entry point for the Ethos music player."""
    ethos_ui = ui.UI()
    ethos_ui.draw_ui()

if __name__ == "__main__":
    sys.exit(main())