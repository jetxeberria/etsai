""" Plugins for managing images. """

from typing import Dict, Callable


def generate() -> None:
    """
    Generate image.
    """
    print("Generating image...")


generate.help_message = "Displays the current system status (CPU, RAM, etc.)."


def register() -> Dict[str, Callable]:
    """
    Registers the available commands for the 'media/image' plugin.

    Returns:
        Dict[str, Callable]: A dictionary of commands.
    """
    return {
        "image-generate": generate
    }
