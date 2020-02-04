from unittest.mock import patch, Mock
from time import sleep
import os
import signal
import select
import pytest
from subprocess import Popen, PIPE
from tests.cli.cli_utils import run_cmd, saga_folder, random_file


#@pytest.fixture(scope="module")
def saga_server():
    # we set up the saga-server
    os.chdir(os.getcwd() + "/saga-server")
    # we set the curr process ID so that killing this group doesn't 
    # kill the testing process as well
    saga_server = Popen(["npm", "start"], preexec_fn=os.setsid, stdout=PIPE, stderr=PIPE)
    sleep(4) # we have to sleep to let the server start
    yield saga_server
    # make sure to kill the server when we are done
    os.killpg(os.getpgid(proc.pid), signal.SIGTERM)

def run_cmd_with_login(cmd, username, password):
    def mock_input(prompt):
        if "username" in prompt.lower():
            return username
        if "password" in prompt.lower():
            return password
    with patch("builtins.input", mock_input):
        out = run_cmd(cmd)
    return out

@pytest.mark.skip("not working")
def test_server(saga_server, saga_folder):
    out = run_cmd_with_login("saga push", "narush", "123")
    print(out)
    assert False