import pytest
from tests.cli.cli_utils import run_cmd, saga_folder, empty_file

def test_log_empty(saga_folder):
    out = run_cmd("saga log")
    expected = """commit: 90a474c02eb88a019c2931ec033f3b704f66a86eba6b81ffa51ba627a59cc8bb\n\tCreated repository\n\n"""
    assert expected in out

def test_log_commit(saga_folder):
    empty_file("temp.txt")
    run_cmd("saga add temp.txt")
    run_cmd("saga commit -m \"add temp.txt\"")
    out = run_cmd("saga log")
    expected = """commit: 987225e7e378689d9de9559b9057ffbbca9ef5d2bf16a398bab55468def19a1e\n\tadd temp.txt\n\ncommit: 90a474c02eb88a019c2931ec033f3b704f66a86eba6b81ffa51ba627a59cc8bb\n\tCreated repository\n\n"""
    assert expected in out