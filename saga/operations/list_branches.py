from saga.Repository1 import Repository1

def list_branches(repository: Repository1):
    """
    Lists the branches in the repo, as well as the head
    """
    for branch in repository.branches:
        if branch == repository.head:
            print("   * {}".format(branch))
        else:
            print("     {}".format(branch))