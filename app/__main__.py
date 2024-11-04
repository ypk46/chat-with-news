# Native imports
import logging

# 3rd party imports
import click

# Project imports
from app.commands import *  # pylint: disable=W0401
from app.config import settings
from app.utils import init_logger

# Initialize logger
logger = logging.getLogger(settings.name)
init_logger(logger, name=settings.name, env=settings.env)


@click.group()
def cli():
    """
    ChatWithNews CLI.
    """


# Add CLI commands
cli.add_command(cmd_serve)

if __name__ == "__main__":
    cli()
