from saga.Repository1 import Repository1
from saga.path_utils import changed_files

def checkout(repository: Repository1, branch_name: str):
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
    inserted, changed, removed = changed_files(repository.base_directory, state_path)
    if any(changed) or any(removed):
        print("Error: please commit or undo changes before switching branches")
        return
    
    repository.set_head(branch_name)

    repository.restore_state(repository.state_hash)

    print("Switched to branch {}".format(branch_name))
    




    """
    if self._uncommited_in_index():
        print("Error: cannot switch branch as there are uncommited changed")
        return

    inserted, changed, removed = changed_files(self.base_directory, self.curr_state_dir())
    if any(changed) or any(removed):
        print("Error: please commit or undo changes before switching branches")
        return

    
    self.head = branch_name
    commit = self.get_commit(self.branches[self.head])        
    self._restore_state(commit.state_hash)
    """
        