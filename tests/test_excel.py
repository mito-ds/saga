import os
import pytest
from tests.test_utils import do_test_merge

def get_test_merges():
    merge_tests = []
    for path in os.listdir("tests/merges/xlsx"):
        path = os.path.join("tests/merges/xlsx", path)
        if os.path.isdir(path):
            merge_tests.append(path)
    return merge_tests
        

@pytest.mark.parametrize("merge_test_name", get_test_merges())
def test_merge(merge_test_name):
    print(os.getcwd())
    assert do_test_merge(merge_test_name, ".xlsx")