import pytest
import os
from copy import deepcopy
from saga.base_file.File import File
from saga.data_types.multi_dim_dict.MultiDimDict import MultiDimDict
from saga.data_types.multi_dim_dict.OP_MDD_Change import OP_MDD_Change
from saga.data_types.multi_dim_dict.OP_MDD_Insert import OP_MDD_Insert
from saga.data_types.multi_dim_dict.OP_MDD_Remove import OP_MDD_Remove

"""
def applies_ops_correctly(l1, l2, dim):
    mdl1 = MultiDimList(l1, dim)
    mdl2 = MultiDimList(l2, dim)

    mdl1_copy = deepcopy(mdl1)
    file = File("id", "type", "name", mdl1_copy)

    ops = mdl1.get_operations(mdl2)

    for op in ops:
        file = op.apply_operation_to_file(file)
    
    applies_forward_correctly = file.file_contents.multi_dim_list == l2

    ops.reverse()
    for op in ops:
        inverse = op.inverse()
        file = inverse.apply_operation_to_file(file)

    applies_backward_correctly = file.file_contents.multi_dim_list == l1

    return applies_forward_correctly and applies_backward_correctly
"""
def test_multi_dim_dict_creation():
    A = {}
    mdd = MultiDimDict(A, 1)
    assert mdd.multi_dim_dict == A
    assert mdd.dimension == 1

def test_get_insert_op_single_key_value():
    dic = {}
    mdd = MultiDimDict(dic, 1)
    mdd.insert_path("", {"key_one" : "val_one"})
    print(mdd.multi_dim_dict)
    assert mdd.multi_dim_dict == {"key_one" : "val_one"}


def test_get_insert_op_multiple_key_value():
    dic = {}
    mdd = MultiDimDict(dic, 1)
    expected_result = {"key_one" : "val_one", "key_two" : "val_two"}
    mdd.insert_path("", expected_result)
    print(mdd.multi_dim_dict)
    assert mdd.multi_dim_dict == expected_result

def test_get_insert_dim_two():
    dic = {"key_one" : {"key_one_dim_two" : "val_one_dim_two"}}
    mdd = MultiDimDict(dic, 2)

    expected_resut = {"key_one" : {"key_one_dim_two" : "val_one_dim_two", "key_two_dim_two" : "val_two_dim_two"}}
    mdd.insert_path(["key_one"], {"key_two_dim_two" : "val_two_dim_two"})
    print(mdd.multi_dim_dict)
    assert mdd.multi_dim_dict == expected_resut

def test_get_insert_dim_three():
    dic = {"key_one" : {"key_one_dim_two" : {"key_one_dim_three" : "val_one_dim_three"}}}
    mdd = MultiDimDict(dic, 3)

    expected_resut = {"key_one" : {"key_one_dim_two" : {"key_one_dim_three" : "val_one_dim_three", "key_two_dim_three" : "val_two_dim_three"}}}
    mdd.insert_path(["key_one", "key_one_dim_two"], {"key_two_dim_three" : "val_two_dim_three"})
    print(mdd.multi_dim_dict)
    assert mdd.multi_dim_dict == expected_resut

def test_get_insert_dim_three_multiple_keys_at_dim_two():
    dic = {"key_one" : {"key_one_dim_two" : {"key_one_dim_three" : "val_one_dim_three"}, "key_two_dim_two" : "val_two_dim_two"}}
    mdd = MultiDimDict(dic, 3)

    expected_resut = {"key_one" : {"key_one_dim_two" : {"key_one_dim_three" : "val_one_dim_three", "key_two_dim_three" : "val_two_dim_three"}, "key_two_dim_two" : "val_two_dim_two"}}
    mdd.insert_path(["key_one", "key_one_dim_two"], {"key_two_dim_three" : "val_two_dim_three"})
    print(mdd.multi_dim_dict)
    assert mdd.multi_dim_dict == expected_resut

def test_get_insert_dim_three_multiple_keys_at_dim_three():
    dic = {"key_one" : {"key_one_dim_two" : {"key_one_dim_three" : "val_one_dim_three", "A" : "B"}}}
    mdd = MultiDimDict(dic, 3)

    expected_resut = {"key_one" : {"key_one_dim_two" : {"key_one_dim_three" : "val_one_dim_three", "key_two_dim_three" : "val_two_dim_three", "A" : "B"}}}
    mdd.insert_path(["key_one", "key_one_dim_two"], {"key_two_dim_three" : "val_two_dim_three"})
    print(mdd.multi_dim_dict)
    assert mdd.multi_dim_dict == expected_resut


def test_get_insert_op_single_key_value():
    dic = {}
    mdd = MultiDimDict(dic, 1)
    mdd.insert_path("", {"key_one_dim_one" : {"key_one_dim_two" : "val_one_dim_two", "key_two_dim_two" : "val_two_dim_two"}})
    print(mdd.multi_dim_dict)
    assert mdd.multi_dim_dict == {"key_one_dim_one" : {"key_one_dim_two" : "val_one_dim_two", "key_two_dim_two" : "val_two_dim_two"}}

"""
def test_get_insert_op_col():
    assert applies_ops_correctly([["A"], ["C"]], [["A", "B"], ["C", "D"]], 2)

def test_get_insert_op_row_and_col():
    assert applies_ops_correctly([["A", "B"], ["C", "D"]], [["A", "B", "X"], ["C", "D", "Y"], ["E", "F", "Z"]], 2)

def test_get_remove_op():
    assert applies_ops_correctly(["A", "B"], ["A"], 1)

def test_get_remove_op_multiple():
    assert applies_ops_correctly(["X", "A", "B", "C", "D"], ["A"], 1)

def test_get_remove_op_row():
    assert applies_ops_correctly([["A", "B"], ["C", "D"]], [["A", "B"]], 2)

def test_get_remove_op_col():
    assert applies_ops_correctly([["A", "B"], ["C", "D"]], [["A"], ["C"]], 2)

def test_get_remove_op_row_and_col():
    assert applies_ops_correctly([["A", "B"], ["C", "D"]], [["A"]], 2)

def test_get_remove_and_insert():
    assert applies_ops_correctly([["A", "B"], ["C", "D"]], [["A", "B"], ["C"], ["F"]], 2)

def test_empty_start():
    assert applies_ops_correctly([], [["A", "B"], ["C"], ["F"]], 2)

def test_empty_end():
    assert applies_ops_correctly([["A", "B"], ["C"], ["F"]], [], 2)

"""

