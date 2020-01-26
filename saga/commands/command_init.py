from os import getcwd
from pathlib import Path
from saga.commands.utils import get_saga_repo_maybe
from saga.operations.init import init


def command_init(args):
    saga_repo = get_saga_repo_maybe()
    if saga_repo is not None:
        print(f"Error: project already exists at {saga_repo.base_directory}")
    else:
        init(Path(getcwd()))
