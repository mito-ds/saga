import pytest
from tests.cli.cli_utils import run_cmd, saga_folder, random_file

def test_log_empty(saga_folder):
    out = run_cmd("saga log")
    expected = """commit: 90a474c02eb88a019c2931ec033f3b704f66a86eba6b81ffa51ba627a59cc8bb\n\tCreated repository\n\n"""
    assert expected in out