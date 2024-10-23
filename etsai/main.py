import typer
from typing import Callable, Dict
from etsai.plugin_loader import load_plugins

import sys

if len(sys.argv) == 1:
    sys.argv.append("--help")


def create_category_app(commands: Dict[str, Callable]) -> typer.Typer:
    """
    Recursively creates a Typer application for a given category with its commands and subcategories.

    Args:
        commands (Dict[str, Callable]): A dictionary of commands or subcategories.

    Returns:
        typer.Typer: A Typer application for the category.
    """
    category_app = typer.Typer()

    @category_app.callback(invoke_without_command=True)
    def show_help(ctx: typer.Context):
        """
        Display help message when no subcommand is provided.
        """
        if ctx.invoked_subcommand is None:
            typer.echo(ctx.get_help())

    for command_name, command_func in commands.items():
        if isinstance(command_func, dict):
            # It's a subcategory; recursively create its Typer app
            sub_category_app = create_category_app(command_func)
            category_app.add_typer(sub_category_app, name=command_name)
        else:
            # It's a command; add it to the current Typer app
            help_message = getattr(
                command_func, 'help_message', f"Command '{command_name}'")
            category_app.command(
                name=command_name, help=help_message)(command_func)

    return category_app


def create_app() -> typer.Typer:
    """
    Creates the main Typer application by loading and registering all plugins.

    Returns:
        typer.Typer: The main Typer application.
    """
    app = typer.Typer()

    plugins = load_plugins()

    for category, commands in plugins.items():
        category_app = create_category_app(commands)
        app.add_typer(category_app, name=category)

    return app


def main():
    """
    Main entry point for the CLI application.
    """
    app = create_app()
    app()


if __name__ == "__main__":
    main()
