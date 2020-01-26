import os
from tests.cli.cli_utils import (
    run_cmd, 
    saga_folder, 
    random_file, 
    current_branch
)


def test_create_branch(saga_folder):
    run_cmd("saga branch newbranch")
    out = run_cmd("saga branch")
    assert "newbranch" in out

def test_switch_branch(saga_folder):
    run_cmd("saga branch newbranch")
    out = run_cmd("saga checkout newbranch")
    print(out)
    out = run_cmd("saga branch")
    out_list = out.split(" ")
    assert "newbranch" in out_list[out_list.index("*") + 1]

def test_cant_switch_uncommitted(saga_folder):
    run_cmd("saga branch newbranch")
    run_cmd("saga checkout newbranch")
    out = run_cmd("saga branch")
    out_list = out.split(" ")
    assert "newbranch" in current_branch()