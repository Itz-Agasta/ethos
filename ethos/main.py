########################
# Entry point of Ethos #
########################

import os
import sys
import platform
from rich.console import Console

sys.path.append(os.getcwd())

def check_audio_output():
    """Check if audio output is available based on platform and environment"""
    console = Console()
    system = platform.system()
    
    # Check if running in headless environment
    is_headless = (
        # Common server/CI environment variables
        "CI" in os.environ or
        "GITHUB_ACTIONS" in os.environ or
        # Check for SSH session
        "SSH_CLIENT" in os.environ or
        "SSH_TTY" in os.environ or
        # Check display for X11
        "DISPLAY" not in os.environ
    )

    if is_headless:
        console.print("[yellow]Warning: Running in a headless environment (possibly a server)")
        console.print("[yellow]Audio output may not be available\n")
        return False

    if system == "Linux":
        # Check for PulseAudio/ALSA
        has_pulse = os.system("which pulseaudio >/dev/null 2>&1") == 0
        has_alsa = os.system("which aplay >/dev/null 2>&1") == 0
        if not (has_pulse or has_alsa):
            console.print("[yellow]Warning: No audio subsystem (PulseAudio/ALSA) detected on Linux")
            console.print("[yellow]Please install PulseAudio or ALSA for audio playback\n")
            return False

    return True

if __name__ == "__main__":
    # Check audio before importing UI modules
    has_audio = check_audio_output()
    
    if not has_audio:
        os.environ["ETHOS_NO_AUDIO"] = "1"
        Console().print("[red]Running in limited mode - audio playback will not be available\n")
        sys.exit(0)  # Exit gracefully in headless environments
    
    from ethos.ui import ui
    ethos_ui = ui.UI()
    ethos_ui.draw_ui()