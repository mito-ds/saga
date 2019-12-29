import pytest
import os
from saga.main import create_parser

def run_cmd(cmd):
    parser = create_parser()
    args = parser.parse_args(args=[cmd])
    args.func(args)

def test_init_creates_folder(tmpdir):
    os.chdir(tmpdir)
    run_cmd("init")
    assert os.path.exists(tmpdir.join(".saga"))


def test_init_fails_existing():
    pass

def test_init_fails_existing_superfolder():
    pass