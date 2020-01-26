from saga.Repository import Repository


def list_branches(repository: Repository):
    """
    Lists the branches in the repo, as well as the head
    """
    for branch in repository.branches:
        if branch == repository.head:
            print("   * {}".format(branch))
        else:
            print("     {}".format(branch))
