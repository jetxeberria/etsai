import typer
from typing import Callable, Dict
from etsai.plugin_loader import load_plugins

def create_category_app(commands: Dict[str, Callable]) -> typer.Typer:
    """
    Creates a Typer app for a given category with its commands.

    Args:
        commands (Dict[str, Callable]): A dictionary of commands or subcategories.

    Returns:
        typer.Typer: A Typer application for the category.
    """
    category_app = typer.Typer()

    for command_name, command_func in commands.items():
        if isinstance(command_func, dict):  # It's a subcategory
            sub_category_app = create_category_app(command_func)
            category_app.add_typer(sub_category_app, name=command_name)
        else:
            help_message = getattr(command_func, 'help_message', f"Command '{command_name}'")
            category_app.command(name=command_name, help=help_message)(command_func)

    return category_app


def app() -> typer.Typer:
    """
    Main function to create the Typer application.

    Returns:
        typer.Typer: The main Typer application.
    """
    app = typer.Typer()

    plugins = load_plugins()

    # Dynamically add categories and commands
    for category, commands in plugins.items():
        category_app = create_category_app(commands)
        app.add_typer(category_app, name=category)

    return app


if __name__ == "__main__":
    typer.run(app)
