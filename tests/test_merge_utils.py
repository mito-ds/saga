import pytest
from saga.base_file.mixed_data_type.merge_utils import merge_rec


def test_list_simple_conflict():
    O = [1]
    A = [1, 2]
    B = [1, 3]

    result = merge_rec(O, A, B)
    assert result == None

def test_list_simple_merge():
    O = [1]
    A = [0, 1]
    B = [1, 2]

    result = merge_rec(O, A, B)
    assert result == [0, 1, 2]

def test_dict_simple_conflict():
    A = {"key": "value"}
    O = {"key": "value1"}
    B = {"key": "value2"}

    result = merge_rec(O, A, B)
    assert result == None

def test_dict_simple_merge():
    O = {"key": "value"}
    A = {"key": "value1"}
    B = {"key": "value"}

    result = merge_rec(O, A, B)
    assert result == {"key": "value1"}


def test_list_complicated_conflict():
    O = [1, 2, 3, 4, 5, 6]
    A = [1, 4, 5, 2, 3, 6]
    B = [1, 2, 4, 5, 3, 6]

    result = merge_rec(O, A, B)
    assert result == None


def test_list_successful_merge():
    O = [1, 2, 6]
    A = [1, 4, 5, 2, 6]
    B = [1, 2, 6]

    result = merge_rec(O, A, B)
    assert result == [1, 4, 5, 2, 6]


def test_multi_dim_merge_easy():
    O = [[1, 2], [3, 4]]
    A = [[1, 2, 3], [3, 4]]
    B = [[1, 2], [3, 4]]

    result = merge_rec(O, A, B)
    assert result == [[1, 2, 3], [3, 4]]


def test_multi_dim_merge_harder():
    O = [[1, 2], [6, 7], [3, 4]]
    A = [[1, 2, 3], [6, 7], [3, 4]]
    B = [[1, 2], [6, 7], [3, 4, 5]]

    result = merge_rec(O, A, B)
    assert result == [[1, 2, 3], [6, 7], [3, 4, 5]]

def test_multi_dim_merge_recursive():
    O = [[1, 2], [6, 7], [3, 4]]
    A = [[1, 2, 3], [6, 7], [3, 4]]
    B = [[0, 1, 2], [6, 7]]

    result = merge_rec(O, A, B)
    assert result == [[0, 1, 2, 3], [6, 7]]


def test_multi_dim_merge_recursive_add_on_end():
    O = [[1, 2], [6, 7]]
    A = [[1, 2, 3], [6, 7], [3, 4]]
    B = [[0, 1, 2], [6, 7], [3, 4]]

    result = merge_rec(O, A, B)
    assert result == None

def test_easy_multi_dim_dict():
    O = {"key": {"key": "value"}}
    A = {"key": {"key": "value1"}}
    B = {"key": {"key": "value"}}

    result = merge_rec(O, A, B)
    assert result == {"key": {"key": "value1"}}

def test_conflict_multi_dim_dict():
    O = {"key": {"key": "value"}}
    A = {"key": {"key": "value1"}}
    B = {"key": {"key": "value2"}}

    result = merge_rec(O, A, B)
    assert result == None

def test_harder_multi_dim_dict():
    O = {"key": {"key": "value"}, "key1": {"key": "value"}}
    A = {"key": {"key": "value"}}
    B = {"key": {"key": "value2"}}

    result = merge_rec(O, A, B)
    assert result == {"key": {"key": "value2"}}

def test_list_of_dicts():
    O = [{"key": "value"}, {"key1": "value"}, {"key2": "value"}]
    A = [{"key": "value1"}, {"key1": "value"}, {"key2": "value"}]
    B = [{"key": "value"}, {"key1": "value1"}, {"key2": "value"}]

    result = merge_rec(O, A, B)
    assert result == [{"key": "value1"}, {"key1": "value1"}, {"key2": "value"}]


def test_dict_of_lists():
    O = {"key": [1]}
    A = {"key": [0, 1]}
    B = {"key": [1, 2]}

    result = merge_rec(O, A, B)
    assert result == {"key": [0, 1, 2]}

def test_dict_of_lists_of_dicts():
    O = {"key": [{"key": "value"}, {"key1": "value"}, {"key2": "value"}]}
    A = {"key": [{"key": "value1"}, {"key1": "value"}, {"key2": "value"}]}
    B = {"key": [{"key": "value"}, {"key1": "value1"}, {"key2": "value"}]}

    result = merge_rec(O, A, B)
    assert result == {"key": [{"key": "value1"}, {"key1": "value1"}, {"key2": "value"}]}