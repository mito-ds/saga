from shutil import copyfile
from saga.Repository1 import Repository1

def create_branch(repository: Repository1, branch_name: str):
        """
        If branch_name does not exist, will create a new branch with this name, 
        branching off from the current commit on head
        """
        if (repository.branch_directory / branch_name).exists():
            print("Error: branch {} already exists".format(branch_name))
        
        head = repository.branch_directory / repository.head
        copyfile(head, repository.branch_directory / branch_name)