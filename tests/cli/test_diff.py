import pytest
from tests.cli.cli_utils import run_cmd, saga_folder, random_file

def test_diff_empty(saga_folder):
    out = run_cmd("saga diff")
    assert out == "Saga diff:\n"