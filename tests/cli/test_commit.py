from tests.cli.cli_utils import run_cmd, saga_folder, random_file

def test_cannot_commit_empty(saga_folder):
    out = run_cmd("saga commit -m \"test\"")
    assert "Error" in out

def test_can_commit_empty_with_flag(saga_folder):
    out = run_cmd("saga commit --allow-empty -m \"test\"")
    assert "Error" not in out