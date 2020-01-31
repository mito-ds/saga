import os
from pathlib import Path
from saga.Repository import Repository


def get_repository():
    repository = get_repository_maybe()
    if repository is None:
        print("Error: command cannot run as no saga repo exists")
        exit(1)
    else:
        return repository


def get_repository_maybe():
    # TODO: rewrite with path.parent and Path.home()

    path = os.getcwd()
    while path != "/":
        # check if there is a
        if os.path.isdir(path + "/.saga"):
            return Repository(Path(path))
        path = os.path.dirname(path)
    return None
