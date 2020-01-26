from saga.Repository import Repository
from saga.path_utils import changed_files


def checkout(repository: Repository, branch_name: str):
    """
    Changes head branch to branch_name.

    Errors if the branch does not exist, or if there
    uncommitted changes in the index, or if there are
    uncommitted changes in the working repository
    to files previously in the state (?)
    """
    if not (repository.branch_directory / branch_name).exists():
        print(f"Error: branch {branch_name} does not exist")
        return

    if repository.uncommited_in_index:
        print(f"Error: uncommitted in index")
        return

    state_path = repository.state_directory / repository.state_hash
    inserted, changed, removed = changed_files(
        repository.base_directory,
        state_path
    )
    if any(changed) or any(removed):
        print("Error: please commit or undo changes before switching branches")
        return

    repository.set_head(branch_name)

    repository.restore_state(repository.state_hash)

    print("Switched to branch {}".format(branch_name))
