import os
from tests.cli.cli_utils import run_cmd, saga_folder, random_file

def test_add_adds_to_index(saga_folder):
    random_file("file")
    run_cmd("saga add file")
    print(os.listdir())
    assert os.path.exists(saga_folder.join(".saga").join("index").join("file"))

def test_add_updates_index(saga_folder):
    random_file("file")
    run_cmd("saga add file")
    assert os.path.exists(saga_folder.join(".saga").join("index").join("file"))
    random_file("file")
    run_cmd("saga add file")
    import filecmp
    index_file = saga_folder.join(".saga").join("index").join("file")
    filecmp.cmp('file', index_file)