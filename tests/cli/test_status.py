import pytest
from tests.cli.cli_utils import run_cmd, saga_folder, random_file

def test_status_empty(saga_folder):
    out = run_cmd("saga status")
    assert out == """On branch master\nChanges staged for commit:\nChange not staged for commit:\nUntracked files:\n"""
    random_file("tmp.txt")
    out = run_cmd("saga status")
    assert out == """On branch master\nChanges staged for commit:\nChange not staged for commit:\nUntracked files:\n\ttmp.txt\n"""
    run_cmd("saga add tmp.txt")
    out = run_cmd("saga status")
    assert out == """On branch master\nChanges staged for commit:\n\tinserted: tmp.txt\nChange not staged for commit:\nUntracked files:\n"""
    run_cmd("saga commit -m \"add tmp.txt\"")
    random_file("tmp.txt")
    out = run_cmd("saga status")
    assert out == """On branch master\nChanges staged for commit:\nChange not staged for commit:\n\tmodified: tmp.txt\nUntracked files:\n"""
    