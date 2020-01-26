import pytest
import os
from tests.cli.cli_utils import run_cmd

def test_init_creates_folder(tmpdir):
    os.chdir(tmpdir)
    out = run_cmd("saga init")
    assert "Created" in out
    assert os.path.exists(tmpdir.join(".saga"))

def test_init_fails_existing(tmpdir):
    os.chdir(tmpdir)
    run_cmd("saga init")
    out = run_cmd("saga init")
    assert "Error" in out

def test_init_fails_existing_superfolder(tmpdir):
    os.chdir(tmpdir)
    run_cmd("saga init")
    subdir = tmpdir.join("/sub")
    os.mkdir(subdir)
    os.chdir(subdir)
    out = run_cmd("saga init")
    assert "Error" in out