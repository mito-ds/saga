import sys
import os
import pytest
import shlex
from unittest.mock import patch
from saga.main import main
from io import StringIO

def run_cmd(cmd):
    cmd_tokens = shlex.split(cmd)
    # mock the input for the parser
    with patch.object(sys, 'argv', cmd_tokens):
        # capture the output 
        with patch.object(sys, "stdout", StringIO()):
            main()
            out = sys.stdout.getvalue()
            sys.stdout.close()
    return out

@pytest.yield_fixture
def saga_folder(tmpdir):
    og_dir = os.getcwd()
    os.chdir(tmpdir)
    run_cmd("saga init")
    yield tmpdir
    os.chdir(og_dir)

def random_file(file_name):
    with open(file_name, 'wb+') as fout:
        fout.write(os.urandom(1024))

def current_branch():
    out = run_cmd("saga branch")
    out_list = out.split(" ")
    return out_list[out_list.index("*") + 1]