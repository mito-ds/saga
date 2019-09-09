import pytest
from saga.merge_utils import diff3

def test_diff3_from_paper_merge_conflict():
    A = [1,4,5,2,3,6]
    O = [1,2,3,4,5,6]
    B = [1,2,4,5,3,6]

    result = diff3(A, O, B)
    print(result)
    assert result == ("conflicting", [(3, ([3], [3,4,5], [4,5,3]))])

def test_diff3_successful_merge():
    A = [1,4,5,2,6]
    O = [1,2,6]
    B = [1,2,6]

    result = diff3(A, O, B)
    print(result)
    assert result == ("merged", [1, 4, 5, 2, 6])
