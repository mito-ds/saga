from os import getcwd
from pathlib import Path
from saga.commands.utils import get_repository_maybe
from saga.operations.init import init


def command_init(args):
    repository = get_repository_maybe()
    if repository is not None:
        print(f"Error: project already exists at {repository.base_directory}")
    else:
        init(Path(getcwd()))
