import pytest
from saga.data_types.multi_dim_list.mdl_merge_utils import diff3



def test_diff3_from_paper_merge_conflict():
    A = [1,4,5,2,3,6]
    O = [1,2,3,4,5,6]
    B = [1,2,4,5,3,6]

    result = diff3(A, O, B, 1)
    assert result == None


def test_diff3_successful_merge():
    A = [1,4,5,2,6]
    O = [1,2,6]
    B = [1,2,6]

    result = diff3(A, O, B, 1)
    assert result == [1, 4, 5, 2, 6]


def test_multi_dim_merge_easy():
    A = [[1, 2, 3], [3, 4]]
    O = [[1, 2], [3, 4]]
    B = [[1, 2], [3, 4]]

    result = diff3(A, O, B, 2)
    assert result == [[1, 2, 3], [3, 4]]


def test_multi_dim_merge_harder():
    A = [[1, 2, 3], [6, 7], [3, 4]]
    O = [[1, 2], [6, 7], [3, 4]]
    B = [[1, 2], [6, 7], [3, 4, 5]]

    result = diff3(A, O, B, 2)
    assert result == [[1, 2, 3], [6, 7], [3, 4, 5]]
