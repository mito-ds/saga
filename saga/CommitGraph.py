NEED_MERGE = True


class CommitGraph(object):

    def __init__(self, repository):
        self.repository = repository

    def least_common_ancestors(self, commit_hash_1, commit_hash_2):
        # returns a list of all the common ancestors of commits
        lca = set()

        # first, we walk all the ancestors of the first commit hash
        current = {commit_hash_1}
        reached = set()
        while any(current):
            curr = current.pop()
            # subtree
            if curr == commit_hash_2:
                return not NEED_MERGE, {curr}
            if curr not in reached:
                reached.add(curr)
                curr_commit = self.repository.get_commit(curr)
                current.update(set(curr_commit.parent_commit_hashes))

        # then we walk the ancestors of the second commit hash
        current = {commit_hash_2}
        while any(current):
            curr = current.pop()
            # in this case (one branch is subbranch of the other)
            # we can just return this single commit
            if curr == commit_hash_1:
                return not NEED_MERGE, {commit_hash_1}
            if curr in reached:
                lca.add(curr)
            else:
                curr_commit = self.repository.get_commit(curr)
                current.update(set(curr_commit.parent_commit_hashes))

        return NEED_MERGE, lca
