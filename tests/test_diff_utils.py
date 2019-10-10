import pytest
from saga.base_file.mixed_data_type.diff_utils import inserted_paths, changed_paths, removed_paths
from saga.base_file.mixed_data_type.lcs import lcs_multi_dimension

def check_ops(A, B, num_removed, num_changed, num_inserted):
    removed = removed_paths(A, B)
    changed = changed_paths(A, B)
    inserted = inserted_paths(A, B)

    assert len(removed) == num_removed
    assert len(changed) == num_changed
    assert len(inserted) == num_inserted

def test_list_add_element_end():
    check_ops(["A", "B"], ["A", "B", "C"], 0, 0, 1)

def test_list_add_element_middle():
    check_ops(["A", "C"], ["A", "B", "C"], 0, 0, 1)

def test_list_add_element_start():
    check_ops(["B", "C"], ["A", "B", "C"], 0, 0, 1)

def test_list_add_elements():
    check_ops([], ["A", "B", "C"], 0, 0, 3)

def test_list_rem_element_end():
    check_ops(["A", "B", "C"], ["A", "B"], 1, 0, 0)

def test_list_rem_element_middle():
    check_ops(["A", "B", "C"], ["A", "C"], 1, 0, 0)

def test_list_rem_element_start():
    check_ops(["A", "B", "C"], ["B", "C"], 1, 0, 0)

def test_list_rem_elements():
    check_ops(["A", "B", "C"], [], 3, 0, 0)

def test_list_change_elements():
    check_ops(["AB", "B", "C"], ["A", "B", "C"], 0, 1, 0)

def test_list_all_operations():
    check_ops(["AB", "B", "C"], ["A", "C", "D"], 1, 1, 1)

def test_list_in_list():
    check_ops([[]], [[], []], 0, 0, 1)
    check_ops([[]], [], 1, 0, 0)
    check_ops([["A"]], [["A", "B"]], 0, 0, 1)

def test_list_in_list_change():
    check_ops([[]], [[], []], 0, 0, 1)
    check_ops([[]], [], 1, 0, 0)
    check_ops([["A"]], [["ABC"]], 0, 1, 0)

def test_dict_in_dict():
    check_ops({"key":{"key": "value"}}, {"key":{"key": "value", "key1": "value"}}, 0, 0, 1)
    check_ops({"key":{"key": "value"}}, {}, 1, 0, 0)
    check_ops({"key":{"key": "value"}}, {"key":{"key": "value1"}}, 0, 1, 0)

def test_list_in_dict():
    pass

def test_dict_in_list():
    pass
    
    
