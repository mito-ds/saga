from unittest.mock import patch
from pathlib import Path
import os
from tests.cli.cli_utils import saga_folder, run_cmd, empty_file


def run_cmd_with_login(cmd, username, password):
    def mock_input(prompt):
        if "username" in prompt.lower():
            return username
        if "password" in prompt.lower():
            return password
    with patch("builtins.input", mock_input):
        out = run_cmd(cmd)
    return out


def test_push_empty(saga_folder):
    run_cmd("saga remote https://sagalab.org")
    # TODO: add fake credentials not on git
    out = run_cmd_with_login("saga push", "narush", "123")
    assert f"Pushed {Path(saga_folder).name} to https://sagalab.org" in out

def test_push_and_clone_empty(tmpdir, saga_folder):
    run_cmd("saga remote https://sagalab.org")
    # TODO: add fake credentials not on git
    out = run_cmd_with_login("saga push", "narush", "123")
    os.chdir(tmpdir)
    out = run_cmd(f"saga clone https://sagalab.org/{Path(saga_folder).name}.saga")
    assert f"Cloned https://sagalab.org/{Path(saga_folder).name}.saga" in out
    assert Path(Path(saga_folder).name).exists()

def test_push_and_clone_file(tmpdir, saga_folder):
    run_cmd("saga remote https://sagalab.org")
    empty_file("tmp.txt")
    run_cmd("saga add tmp.txt")
    run_cmd("saga commit -m \"add tmp.txt\"")
    # TODO: add fake credentials not on git
    out = run_cmd_with_login("saga push", "narush", "123")
    os.chdir(tmpdir)
    out = run_cmd(f"saga clone https://sagalab.org/{Path(saga_folder).name}.saga")
    assert f"Cloned https://sagalab.org/{Path(saga_folder).name}.saga" in out
    assert Path(Path(saga_folder).name).exists()
    os.chdir(Path(tmpdir) / Path(saga_folder).name)
    out = run_cmd("saga log")
    assert "add tmp.txt" in out
