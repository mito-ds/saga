import os
from saga.Commit import Commit

class CommitGraph(object):

    def __init__(self, commit_directory):
        self.commit_directory = commit_directory

    def least_common_ancestors(self, commit_hash_1, commit_hash_2):
        # returns a list of all the common ancestors of commits
        lca = set()

        # first, we walk all the ancestors of the first commit hash
        current = {commit_hash_1}
        reached = set()
        while any(current):
            curr = current.pop()
            if curr not in reached:
                reached.add(curr)
                curr_commit = self.get_commit(curr)
                current.update(set(curr_commit.parent_commit_hashes))
        
        # then we walk the ancestors of the second commit hash
        current = {commit_hash_2}
        while any(current):
            curr = current.pop()
            if curr in reached:
                lca.add(curr)
            else:
                curr_commit = self.get_commit(curr)
                current.update(set(curr_commit.parent_commit_hashes))
        
        return lca


    def get_commit(self, commit_hash):
        f = open(os.path.join(self.commit_directory, commit_hash), "rb")
        commit_bytes = f.read()
        f.close()
        return Commit.from_bytes(commit_bytes)


    