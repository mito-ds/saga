import pytest
from tests.cli.cli_utils import run_cmd, saga_folder, empty_file

def test_state_hash(saga_folder):
    empty_file("file.rtf")
    run_cmd("saga add file.rtf")
    run_cmd("saga commit -m \"first commit \"")
    out = run_cmd("saga state_hash master")
    expected = "0f745679e632c1990731a790e486a78fb624a16700fbf0d245d8c520b09edb6f"
    assert expected in out