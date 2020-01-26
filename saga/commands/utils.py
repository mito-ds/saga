import os
import argparse
from saga.Repository import Repository

def get_saga_repo():
    saga_repo = get_saga_repo_maybe()
    if saga_repo is None:
        print("Error: command cannot run as no saga repo exists")
        exit(1)
    else:
        return saga_repo

def get_saga_repo_maybe():
    path = os.getcwd()
    while path != "/":
        # check if there is a
        if os.path.isdir(path + "/.saga"):
            return Repository.read(path) 
        path = os.path.dirname(path)
    return None

def get_saga_repo1():
    saga_repo = get_saga_repo_maybe1()
    if saga_repo is None:
        print("Error: command cannot run as no saga repo exists")
        exit(1)
    else:
        return saga_repo

def get_saga_repo_maybe1():
    # TODO: rewrite with path.parent and Path.home()

    path = os.getcwd()
    while path != "/":
        # check if there is a
        if os.path.isdir(path + "/.saga"):
            from saga.Repository1 import Repository1
            from pathlib import Path
            return Repository1(Path(path))
        path = os.path.dirname(path)
    return None