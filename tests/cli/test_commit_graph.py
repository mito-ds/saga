import os
from pathlib import Path
from tests.cli.cli_utils import run_cmd, saga_folder, random_file
from saga.CommitGraph import CommitGraph
from saga.Repository import Repository

def partial_to_full_hash(saga_folder, partial_hash):
    for path in os.listdir(os.path.join(saga_folder, ".saga", "commits")):
        if path.startswith(partial_hash):
            return path
    return None

def partial_hash_from_blurb(commit_blurb):
    return str(commit_blurb[1:13])

def blurb_to_hash(saga_folder, commit_blurb):
    return partial_to_full_hash(
        saga_folder, 
        partial_hash_from_blurb(commit_blurb)
    )

def test_lca_simple(tmpdir):
    # setup saga and get init hash
    os.chdir(tmpdir)
    init_blurb = run_cmd("saga init")
    init_hash = blurb_to_hash(str(tmpdir), init_blurb)
    # make a branch a and b
    run_cmd("saga branch a")
    run_cmd("saga branch b")
    # make one commit on a
    run_cmd("saga checkout a")
    a_blurb = run_cmd("saga commit --allow-empty -m \"ack\"")
    a_hash = blurb_to_hash(str(tmpdir), a_blurb)
    # make one commit on b
    run_cmd("saga checkout b")
    b_blurb = run_cmd("saga commit --allow-empty -m \"back\"")
    b_hash = blurb_to_hash(str(tmpdir), b_blurb)
    # check that the lca is the initial commit, from both
    repo = Repository(Path(tmpdir))
    commit_graph = CommitGraph(repo)
    need_merge, lcas = commit_graph.least_common_ancestors(a_hash, b_hash)
    assert len(lcas) == 1
    assert lcas.pop() == init_hash


def test_lca_merge(tmpdir):
    # setup saga and get init hash
    os.chdir(tmpdir)
    init_blurb = run_cmd("saga init")
    init_hash = blurb_to_hash(str(tmpdir), init_blurb)
    # make a branch a1, a2, and b
    run_cmd("saga branch a1")
    run_cmd("saga branch a2")
    run_cmd("saga branch b")
    # make one commit on a1 and a2
    run_cmd("saga checkout a1")
    run_cmd("saga commit --allow-empty -m \"ack\"")
    # but we add a random file on a2 so the commit has is different
    run_cmd("saga checkout a2")
    random_file("file")
    run_cmd("saga add file")
    run_cmd("saga commit -m \"ack\"")
    # and then merge them 
    merge_blurb = run_cmd("saga merge a1")
    merge_hash = blurb_to_hash(str(tmpdir), merge_blurb)
    # make one commit on b
    run_cmd("saga checkout b")
    b_blurb = run_cmd("saga commit --allow-empty -m \"back\"")
    b_hash = blurb_to_hash(str(tmpdir), b_blurb)
    # check that the lca is the initial commit, from both
    repo = Repository(Path(tmpdir))
    repo.debug()
    commit_graph = CommitGraph(repo)
    need_merge, lcas = commit_graph.least_common_ancestors(merge_hash, b_hash)
    assert len(lcas) == 1
    assert lcas.pop() == init_hash


def test_lca_two(tmpdir):
    # setup saga and get init hash
    os.chdir(tmpdir)
    run_cmd("saga init")
    # make a branch a and b
    run_cmd("saga branch a")
    run_cmd("saga branch b")
    # make one commit on a
    run_cmd("saga checkout a")
    random_file("filea")
    run_cmd("saga add filea")
    a_blurb = run_cmd("saga commit -m \"ack\"")
    a_commit = blurb_to_hash(str(tmpdir), a_blurb)
    # make one commit on b
    run_cmd("saga checkout b")
    random_file("fileb")
    run_cmd("saga add fileb")
    b_blurb = run_cmd("saga commit -m \"ack\"")
    b_commit = blurb_to_hash(str(tmpdir), b_blurb)
    # merge from b to a
    b_merge_blurb = run_cmd("saga merge a")
    b_merge_hash = blurb_to_hash(str(tmpdir), b_merge_blurb)
    # merge from a to b
    run_cmd("saga checkout a")
    # TODO: we cannot do this currently, as we have no ability to 
    # merge in remote branches -- or merge in by commit hash
    # (which we should have...)
    return
    a_merge_blurb = run_cmd("saga merge b")
    a_merge_hash = blurb_to_hash(str(tmpdir), a_merge_blurb)
    # check that we get two common ancestors
    commit_graph = CommitGraph(os.path.join(tmpdir, ".saga", "commits"))
    lcas = commit_graph.least_common_ancestors(b_merge_hash, a_merge_hash)
    assert len(lcas) == 2
    assert a_commit in lcas and b_commit in lcas


