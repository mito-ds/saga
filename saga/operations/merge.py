from saga.path_utils import changed_files
from saga.Repository import Repository
from saga.CommitGraph import CommitGraph
from saga.file_types.file_utils import parse_file, write_file
from saga.operations.add import add
from saga.operations.commit import commit


def fast_forward(repository: Repository, other_branch: str):
    # Get the head commit on the other branch
    other_branch_head_hash = repository.head_commit_from_branch(other_branch)
    if other_branch_head_hash is None:
        print(f"Error: cannot fast forward as {other_branch} has no head")
        exit(1)

    other_branch_head_commit = repository.get_commit(other_branch_head_hash)
    repository.update_head_commit(other_branch_head_commit)
    repository.restore_state(other_branch_head_commit.state_hash)
    print(f"Fast-forward branch {repository.head} to branch {other_branch}")


def merge(repository: Repository, other_branch: str):
    """
    Merges current head with a other_branch
    """
    if other_branch not in repository.branches:
        print(
            f"Error: cannot merge branch \
            {other_branch} as it does not exist"
        )
        return

    # get the two commit hashes to find the common ancestor of
    commit_hash_1 = repository.head_commit_hash
    commit_hash_2 = repository.head_commit_from_branch(other_branch)

    # get their least common ancestor commit hashes
    commit_graph = CommitGraph(repository)
    need_merge, lcas = commit_graph.least_common_ancestors(
        commit_hash_1,
        commit_hash_2
    )

    if not need_merge:
        assert len(lcas) == 1
        if lcas.pop() == commit_hash_1:
            fast_forward(repository, other_branch)
        else:
            print(f"Branch {other_branch} is a subbranch of {repository.head}")
    else:
        # for now, we are gonna assume there is one lca
        lca = lcas.pop()
        state_dir_old = repository.state_directory / \
            repository.get_commit(lca).state_hash
        state_dir_newA = repository.state_directory / repository.state_hash
        state_dir_newB = repository.state_directory / \
            repository.get_commit(commit_hash_2).state_hash

        removed_paths_A, changed_paths_A, inserted_paths_A = changed_files(
            state_dir_old,
            state_dir_newA
        )
        removed_paths_B, changed_paths_B, inserted_paths_B = changed_files(
            state_dir_old,
            state_dir_newB
        )

        possibly_mergable = set()
        for path in removed_paths_A.intersection(changed_paths_B):
            print(
                f"Confict as {path} was removed in \
                {repository.head} and modified in {other_branch}"
            )
        for path in removed_paths_B.intersection(changed_paths_A):
            print(
                f"Confict as {path} was removed in \
                {repository.head} and modified in {other_branch}"
            )
        for path in changed_paths_A.intersection(changed_paths_B):
            possibly_mergable.add(path)
        for path in inserted_paths_A.intersection(inserted_paths_B):
            print(
                f"Conflict as {path} was inserted in \
                both {repository.head} and {other_branch}"
            )

        # we only write the files if there are no merge conflicts in any
        files_to_write = []
        for path in possibly_mergable:
            file_o = parse_file("TEMP", path, state_dir_old / path)
            file_a = parse_file("TEMP", path, state_dir_newA / path)
            file_b = parse_file("TEMP", path, state_dir_newB / path)

            merge_file = file_o.merge(file_a, file_b, path)
            if merge_file is None:
                print(f"Merge conflict for file {file_o.file_name}")
                return
            else:
                print(f"Successfully merged file {file_o.file_name}")
                files_to_write.append(merge_file)
        for f in files_to_write:
            write_file(f)
            add(repository, f.file_path)
        commit(
            repository,
            f"Merged {other_branch} into branch {repository.head}",
            allow_empty=True
        )
