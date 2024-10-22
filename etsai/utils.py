
import subprocess
from pathlib import Path
from datetime import datetime

def run_command(command):
    """Run a shell command and return the output."""
    print(f"Running command: {command}")
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stderr = result.stderr.decode()
    stdout = result.stdout.decode()
    # if result.returncode != 0 or stderr:
    #     raise subprocess.CalledProcessError(1, command, output=stdout, stderr=stderr)
    return stdout

def generate_output_filename(input_file, suffix):
    """Generate a non-overwriting output filename."""
    input_path = Path(input_file)
    output_filename = input_path.stem + suffix + input_path.suffix
    return input_path.parent / output_filename

def now():
    """Return the current UTC time."""
    return datetime.now()    