import pytest
from saga.merge_utils import diff3

def test_diff3_from_paper():
    A = [1,4,5,2,3,6]
    O = [1,2,3,4,5,6]
    B = [1,2,4,5,3,6]

    result = diff3(A, O, B)
    print(result)
    assert result == [([1], [1], [1]), ([4, 5], [4, 5], [4, 5]), ([2], [2], [2]), ([3], [3, 4, 5], [4, 5, 3]), ([6], [6], [6])]