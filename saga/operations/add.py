import os
from pathlib import Path
from shutil import copyfile
from saga.Repository1 import Repository1
from saga.path_utils import copy_dir_to_dir


def add(repository: Repository1, add_path: str):
    
    add_path = Path(add_path)

    if not add_path.exists():
        print(f"Error: path {add_path} does not exist")
        return

    if add_path.is_file():
        copyfile(add_path, repository.index_directory / add_path)
    else:
        copy_dir_to_dir(
            add_path,
            repository.index_directory,
            exclude=[".saga"]
        )
