import pytest
import os
from tests.cli.cli_utils import saga_folder, run_cmd

def test_init_has_no_remote(saga_folder):
    out = run_cmd("saga remote")
    assert "localhost" in out

def test_set_remote_has_remote(saga_folder):
    out = run_cmd("saga remote testing")
    assert "testing" in out
    out = run_cmd("saga remote")
    assert "testing" in out
