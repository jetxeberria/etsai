""" Plugins for managing system. """

from typing import Dict, Callable

def check_status() -> None:
    """
    Checks and prints the current system status.
    """
    print("Checking system status...")

check_status.help_message = "Displays the current system status (CPU, RAM, etc.)."

def register() -> Dict[str, Callable]:
    """
    Registers the available commands for the 'status' plugin.

    Returns:
        Dict[str, Callable]: A dictionary of commands.
    """
    return {
        "status": check_status
    }
