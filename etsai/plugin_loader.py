import importlib.util
import os
import typer
from typing import Dict, Callable


def load_plugins_recursive(plugins_dir: str) -> Dict[str, Dict[str, Callable]]:
    """
    Recursively loads plugins from the given directory.

    Args:
        plugins_dir (str): Path to the plugins directory.

    Returns:
        Dict[str, Dict[str, Callable]]: A dictionary where keys are categories or commands, 
        and values are subcategories or command functions.
    """
    plugins = {}

    for item in os.listdir(plugins_dir):
        item_path = os.path.join(plugins_dir, item)

        if os.path.isdir(item_path):
            sub_plugins = load_plugins_recursive(item_path)
            if sub_plugins:
                plugins[item] = sub_plugins

        elif item.endswith('.py') and not item.startswith('__'):
            module_name = item[:-3]
            try:
                spec = importlib.util.spec_from_file_location(
                    module_name, item_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                if hasattr(module, 'register'):
                    registered_commands = module.register()
                    if isinstance(registered_commands, dict):
                        plugins.update(registered_commands)
                    else:
                        print(f"Warning: The plugin '{
                              item}' did not return a dictionary in 'register()'.")
                else:
                    print(f"Warning: The plugin '{
                          item}' does not have a 'register()' function.")
            except Exception as e:
                print(f"Error loading the plugin '{item}': {e}")

    return plugins


def load_plugins(plugins_dir: str = None) -> Dict[str, Dict[str, Callable]]:
    """
    Loads all plugins from the root plugins directory.

    Args:
        plugins_dir (str, optional): Path to the plugins directory. Defaults to './plugins'.

    Returns:
        Dict[str, Dict[str, Callable]]: A dictionary with all the loaded plugins.
    """
    if plugins_dir is None:
        plugins_dir = os.path.join(os.path.dirname(__file__), 'plugins')

    if not os.path.exists(plugins_dir) or not os.path.isdir(plugins_dir):
        raise ValueError(f"The specified directory '{
                         plugins_dir}' does not exist or is not valid.")

    return load_plugins_recursive(plugins_dir)
