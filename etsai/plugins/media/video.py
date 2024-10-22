""" Plugins for managing videos. """

from typing import Dict, Callable

def convert() -> None:
    """
    Convert video.
    """
    print("Converting video...")

convert.help_message = "Convert video."

def register() -> Dict[str, Callable]:
    """
    Registers the available commands for the 'media/video' plugin.

    Returns:
        Dict[str, Callable]: A dictionary of commands.
    """
    return {
        "video-convert": convert
    }
