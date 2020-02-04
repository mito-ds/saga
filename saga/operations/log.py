from saga.Repository import Repository

def log(repository: Repository):
    """
    Prints all commits in the current branch to the screen
    """

    curr_commits = [repository.get_commit(repository.head_commit_hash)]

    for commit in curr_commits:
        if commit is not None:
            print("commit: {}".format(commit.hash))
            print("\t{}\n".format(commit.commit_message))
            parent_commits = [
                repository.get_commit(parent_commit_hash)
                for parent_commit_hash in commit.parent_commit_hashes
                if parent_commit_hash is not None
            ]
            curr_commits.extend(parent_commits)