import pytest
from tests.cli.cli_utils import run_cmd, saga_folder, empty_file

def test_state_hash_master(saga_folder):
    empty_file("file.rtf")
    run_cmd("saga add file.rtf")
    run_cmd("saga commit -m \"first commit \"")
    out = run_cmd("saga state_hash master")
    expected = "0f745679e632c1990731a790e486a78fb624a16700fbf0d245d8c520b09edb6f"
    assert expected in out

def test_state_hash_branch(saga_folder):
    empty_file("file.rtf")
    run_cmd("saga add file.rtf")
    run_cmd("saga commit -m \"first commit \"")
    run_cmd("saga branch branchOne")
    run_cmd("saga checkout branchOne")
    out = run_cmd("saga state_hash branchOne")
    expected = "0f745679e632c1990731a790e486a78fb624a16700fbf0d245d8c520b09edb6f"
    assert expected in out