from os import mkdir
from typing import List
from saga.Repository import Repository
from saga.path_utils import copy_dir_to_dir


def commit_int(
        repository: Repository,
        commit_message: str,
        parent_commit_hashes: List[str],
        allow_empty: bool = False
        ):
    """
    Creates a new commit with commit_messages off the parent commit hashes

    TODO: list error conditions
    """
    if not allow_empty and not repository.uncommited_in_index:
        print("Error: no changes to commit")
        return

    # get the information for the commit
    state_hash = repository.index_hash

    # copy the index folder to a new state folder
    state_dir = repository.state_directory / repository.index_hash
    # we don't need to copy if it already exists
    if not state_dir.is_dir():
        mkdir(state_dir)
        copy_dir_to_dir(repository.index_directory, state_dir)

    # add the commit to the commit db
    commit = repository.add_commit(
        state_hash,
        parent_commit_hashes,
        commit_message
    )

    if commit is None:
        print("Error: could not create new commit")
        exit(1)

    # update the head commit of the head branch
    repository.update_head_commit(commit)

    # print that the commit was successful
    print("[{}] {}".format(commit.hash[0:12], commit_message))


def commit(
        repository: Repository,
        commit_message: str,
        allow_empty: bool = False
        ):
    """
    Creates a new commit with commit_messages on the HEAD branch.

    TODO: list error conditions
    """

    # get the information for the commit
    head_commit_hash = repository.head_commit_hash

    commit_int(
        repository,
        commit_message,
        [head_commit_hash],
        allow_empty=allow_empty
    )
