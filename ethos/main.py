########################
# Entry point of Ethos #
########################

import os
import sys
sys.path.append(os.getcwd())

from ui import ui

if __name__ == "__main__":
    ethos_ui = ui.UI()
    ethos_ui.draw_ui()
