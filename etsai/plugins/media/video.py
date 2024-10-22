""" Plugins for managing videos. """

import typer
from etsai.utils import run_command, generate_output_filename, now
from typing import Dict, Callable
from datetime import datetime

def convert() -> None:
    """
    Convert video.
    """
    print("Converting video...")

convert.help_message = "Convert video."

def validate_time_format(time_str: str) -> bool:
    """
    Validate the time format (HH:MM:SS).
    
    Args:
        time_str (str): The time string to validate.
    
    Returns:
        bool: True if valid, False otherwise.
    """
    try:
        datetime.strptime(time_str, "%H:%M:%S")
        return True
    except ValueError:
        return False

def trim(
    file: str = typer.Option(..., "-f", "--file", help="Input video file"),
    start_time: str = typer.Option(None, "--start-time", help="Start time (e.g., 00:00:13)"),
    stop_time: str = typer.Option(None, "--stop-time", help="Stop time (e.g., 00:01:00)"),
    output: str = typer.Option(None, "-o", "--output", help="Output video file"),
):
    """
    Trim a video file. Specify either start-time, stop-time, or both.
    """
    if not start_time and not stop_time:
        raise typer.BadParameter("At least one of --start-time or --stop-time must be provided.")

    if start_time and not validate_time_format(start_time):
        raise typer.BadParameter("Invalid start-time format. Use HH:MM:SS.")

    if stop_time and not validate_time_format(stop_time):
        raise typer.BadParameter("Invalid stop-time format. Use HH:MM:SS.")

    if not output:
        output = generate_output_filename(file, f"_trimmed_{now().isoformat()}")

    command = f"ffmpeg -i {file}"
    if start_time:
        command += f" -ss {start_time}"
    if stop_time:
        command += f" -to {stop_time}"
    command += f" -c copy {output}"
    
    run_command(command)
    typer.echo(f"Video trimmed successfully, saved as: {output}")


def register() -> Dict[str, Callable]:
    """
    Registers the available commands for the 'media/video' plugin.

    Returns:
        Dict[str, Callable]: A dictionary of commands.
    """
    return {
        "video-convert": convert,
        "video-trim": trim
    }
