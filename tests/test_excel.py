import os

def test_merge():
    from tests.test_utils import do_test_merge
    for path in os.listdir("tests/merges/excel"):
        path = os.path.join("tests/merges/excel", path)
        if os.path.isdir(path):
            assert do_test_merge(path, ".xlsx")