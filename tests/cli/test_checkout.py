import os
from tests.cli.cli_utils import (
    run_cmd, 
    saga_folder, 
    random_file, 
    current_branch
)

def test_cannot_checkout_no_branch(saga_folder):
    out = run_cmd("saga checkout newbranch")
    assert "Error" in out

def test_cannot_checkout_create_branch(saga_folder):
    out = run_cmd("saga checkout -b newbranch")
    assert "Error" not in out
    assert "newbranch" in current_branch()

def test_switch_branch_switches_directory(saga_folder):
    run_cmd("saga branch newbranch")
    random_file("file")
    run_cmd("saga add file")
    run_cmd("saga commit -m \"ah\"")
    run_cmd("saga checkout newbranch")
    assert "newbranch" in current_branch()
    assert not os.path.exists(saga_folder.join("file"))

def test_switch_branch_switches_directory_back(saga_folder):
    run_cmd("saga branch newbranch")
    random_file("file")
    run_cmd("saga add file")
    run_cmd("saga commit -m \"ah\"")
    run_cmd("saga checkout newbranch")
    out = run_cmd("saga checkout master")
    assert "master" in current_branch()
    assert os.path.exists(saga_folder.join("file"))

def test_cannot_switch_removed_change(saga_folder):
    run_cmd("saga branch newbranch")
    random_file("file")
    run_cmd("saga add file")
    run_cmd("saga commit -m \"ack\"")
    os.remove("file")
    out = run_cmd("saga checkout newbranch")
    assert "Error" in out

def test_cannot_switch_uncommitted_changes(saga_folder):
    run_cmd("saga branch newbranch")
    random_file("file")
    run_cmd("saga add file")
    out = run_cmd("saga checkout newbranch")
    assert "Error" in out