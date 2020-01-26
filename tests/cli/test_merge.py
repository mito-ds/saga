import os
import pytest
import shutil
import filecmp
from pathlib import Path
from saga.file_types.file_utils import parse_file
from tests.cli.cli_utils import (
    run_cmd, 
    saga_folder, 
    random_file, 
    current_branch
)


def get_test_merges():
    test_merge_names = []
    base = os.path.abspath("tests/merges/")
    for file_type in os.listdir("tests/merges/"):
        merge_file_type = os.path.join(base, file_type)
        if os.path.isdir(merge_file_type):
            for path in os.listdir(merge_file_type):
                path = os.path.join(merge_file_type, path)
                if os.path.isdir(path):
                    test_merge_names.append((path, file_type))

    return test_merge_names
                # we do a merge here


@pytest.mark.parametrize("merge_test_name, file_type", get_test_merges())
def test_merge(saga_folder, merge_test_name, file_type):
    origin = os.path.join(merge_test_name, "origin." + file_type)
    a = os.path.join(merge_test_name, "a." + file_type)
    b = os.path.join(merge_test_name, "b." + file_type)
    merge = os.path.join(merge_test_name, "merge." + file_type)
    file_name = "file." + file_type

    # First, we copy the origin file, and commit it
    shutil.copyfile(origin, saga_folder.join(file_name))
    run_cmd(f"saga add {file_name}")
    run_cmd("saga commit -m \"add file origin\"")

    # then we make branch a and b
    run_cmd("saga branch brancha")
    run_cmd("saga branch branchb")

    # we add file a to branch a
    run_cmd("saga checkout brancha")
    shutil.copyfile(a, file_name)
    run_cmd(f"saga add {file_name}")
    run_cmd("saga commit -m \"add file a\"")

    # we add file b to branch b
    run_cmd("saga checkout branchb")
    shutil.copyfile(b, f"{file_name}")
    run_cmd(f"saga add {file_name}")
    run_cmd("saga commit -m \"add file b\"")

    # then, we try and merge from one branch to the other
    m = run_cmd("saga merge brancha")

    # and check this is the correct merged result
    path = str(saga_folder.join(file_name))
    merge = parse_file("", merge, Path(merge)).file_contents
    assert merge == \
        parse_file("", path, Path(path)).file_contents