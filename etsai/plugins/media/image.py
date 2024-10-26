""" Plugins for managing images. """

from typing import Dict, Callable
import typer


def generate() -> None:
    """
    Generate image.
    """
    print("Generating image...")


generate.help_message = "Displays the current system status (CPU, RAM, etc.)."


def to_text(
    image: str = typer.Option(..., "-f", "--file", help="Input image file"),

) -> None:
    """
    Read image and extract text
    """
    print("Extracting text from image...")
    print(image)


to_text.help_message = "Extract text from an image."


def register() -> Dict[str, Callable]:
    """
    Registers the available commands for the 'media/image' plugin.

    Returns:
        Dict[str, Callable]: A dictionary of commands.
    """
    return {
        "image-generate": generate,
        "image-to-text": to_text
    }
