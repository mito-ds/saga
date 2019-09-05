import pytest
import os
from copy import deepcopy
from saga.base_file.File import File
from saga.data_types.multi_dim_list.MultiDimList import MultiDimList
from saga.data_types.multi_dim_list.OP_MDL_Change import OP_MDL_Change
from saga.data_types.multi_dim_list.OP_MDL_Insert import OP_MDL_Insert
from saga.data_types.multi_dim_list.OP_MDL_Remove import OP_MDL_Remove

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

def test_multi_dim_list_creation():
    A = []
    mdl = MultiDimList(A, 1)
    assert mdl.multi_dim_list == A
    assert mdl.dimension == 1

def test_get_insert_op():
    assert applies_ops_correctly(["A"], ["A", "B"], 1)

def test_get_insert_op_multiple():
    assert applies_ops_correctly(["A"], ["X", "A", "B", "C", "D"], 1)

def test_get_insert_op_row():
    assert applies_ops_correctly([["A", "B"]], [["A", "B"], ["C", "D"]], 2)

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



