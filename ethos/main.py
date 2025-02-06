########################
# Entry point of Ethos #
########################

import os
import sys
from dotenv import load_dotenv
sys.path.append(os.getcwd())

from ethos.ui import ui

def main():
    load_dotenv()
    ethos_ui = ui.UI()
    ethos_ui.draw_ui()
