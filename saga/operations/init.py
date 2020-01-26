from pathlib import Path
from typing import Optional
from saga.Repository import Repository
from saga.operations.commit import commit


def get_saga_repo_path(directory: Path) -> Optional[Path]:
    while directory != Path("/"):
        if (directory / ".saga").is_dir():
            return directory / ".saga"
        directory = directory.parent
    return None


def init(directory: Path):
    """
    Creates a new saga project in the given directory.

    Fails if the given directory is a sub-directory of an existing
    saga project, or if the directory already contains a saga project.
    """
    # ensure this directory isn't inside saga project
    saga_repo_path = get_saga_repo_path(directory)
    if saga_repo_path is not None:
        print(f"Error: saga project already exists at {saga_repo_path}")

    # create empty saga folder, sub-folders
    (directory / ".saga").mkdir()
    (directory / ".saga" / "commits").mkdir()
    (directory / ".saga" / "states").mkdir()
    (directory / ".saga" / "index").mkdir()
    (directory / ".saga" / "branches").mkdir()

    # create the repository container object
    repository = Repository(directory)

    # create an empty commit on the master branch, so no special cases
    commit(
        repository,
        "Created repository",
        allow_empty=True
    )

    # Notify the user of success
    print(f"Initialized empty saga repository in {repository.saga_directory}")
