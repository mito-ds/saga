import os
from pathlib import Path
from saga.Repository import Repository


def get_saga_repo():
    saga_repo = get_saga_repo_maybe()
    if saga_repo is None:
        print("Error: command cannot run as no saga repo exists")
        exit(1)
    else:
        return saga_repo


def get_saga_repo_maybe():
    # TODO: rewrite with path.parent and Path.home()

    path = os.getcwd()
    while path != "/":
        # check if there is a
        if os.path.isdir(path + "/.saga"):
            return Repository(Path(path))
        path = os.path.dirname(path)
    return None
