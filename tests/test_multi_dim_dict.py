import pytest
import os
from copy import deepcopy
from saga.base_file.File import File
from saga.data_types.multi_dim_dict.MultiDimDict import MultiDimDict
from saga.data_types.multi_dim_dict.OP_MDD_Change import OP_MDD_Change
from saga.data_types.multi_dim_dict.OP_MDD_Insert import OP_MDD_Insert
from saga.data_types.multi_dim_dict.OP_MDD_Remove import OP_MDD_Remove

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


def test_get_remove_all_from_single_dim():
    dic = {"key_one_dim_one" : "val_one_dim_one"}
    mdd = MultiDimDict(dic, 1)
    mdd.remove_path(["key_one_dim_one"])
    expected_result = {}
    assert mdd.multi_dim_dict == expected_result

def test_get_remove_all_two_dim():
    dic = {"key_one_dim_one" : {"key_one_dim_two" : "val_one_dim_two", "key_two_dim_two" : "val_two_dim_two"}}
    mdd = MultiDimDict(dic, 2)
    mdd.remove_path(["key_one_dim_one"])
    expected_result = {}
    assert mdd.multi_dim_dict == expected_result

def test_get_remove_single_multiple_dims():
    dic = {"key_one_dim_one" : {"key_one_dim_two" : {"key_one_dim_three" : "val_one_dim_three", "key_two_dim_three" : "val_two_dim_three", "A" : "B"}, "key_should_remain" : "val_should_remain"}}
    mdd = MultiDimDict(dic, 3)
    mdd.remove_path(["key_one_dim_one", "key_one_dim_two"])
    expected_result = {"key_one_dim_one" : {"key_should_remain" : "val_should_remain"}}
    assert mdd.multi_dim_dict == expected_result

def test_insert_and_remove():
    dic = {}
    mdd = MultiDimDict(dic, 1)
    mdd.insert_path([], {"key_one_dim_two" : "val_one_dim_two", "key_two_dim_two" : "val_two_dim_two"})
    mdd.remove_path(["key_two_dim_two"])
    assert mdd.multi_dim_dict == {"key_one_dim_two" : "val_one_dim_two"}

def test_change_single_value():
    dic = {"key_one_dim_one" : "val_one_dim_one"}
    mdd = MultiDimDict(dic, 1)
    mdd.change_value(["key_one_dim_one"], "new_value")
    assert mdd.multi_dim_dict == {"key_one_dim_one" : "new_value"}

def test_change_single_value_to_dict():
    dic = {"key_one_dim_one" : "val_one_dim_one"}
    mdd = MultiDimDict(dic, 1)
    mdd.change_value(["key_one_dim_one"], {"key_one_dim_two" : "val_one_dim_two"})
    assert mdd.multi_dim_dict == {"key_one_dim_one" : {"key_one_dim_two" : "val_one_dim_two"}}

def test_change_dim_two():
    dic = {"key_one_dim_one" : {"key_one_dim_two" : "val_one_dim_two", "key_two_dim_two" : "val_two_dim_two"}}
    mdd = MultiDimDict(dic, 1)
    mdd.change_value(["key_one_dim_one", "key_one_dim_two"], {"key_one_dim_three" : "val_one_dim_three"})
    print(mdd.multi_dim_dict)
    assert mdd.multi_dim_dict == {"key_one_dim_one" : {"key_one_dim_two" : {"key_one_dim_three" : "val_one_dim_three"}, "key_two_dim_two" : "val_two_dim_two"}}
    

def test_get_operations_single_insert():
    dic_old = {"key_one_dim_one" : "val_one_dim_one"}
    dic_new = {"key_one_dim_one" : "val_one_dim_one", "key_two_dim_one" : "val_two_dim_one"}
    mdd_old = MultiDimDict(dic_old, 1)
    mdd_new = MultiDimDict(dic_new, 1)

    operations = mdd_new.get_operations(mdd_old)
    assert isinstance(operations[0], OP_MDD_Insert)
    assert operations[0].path == []
    assert operations[0].value == {"key_two_dim_one" : "val_two_dim_one"}


def test_get_operations_multiple_inserts_dim_one():
    dic_old = {"key_one_dim_one" : "val_one_dim_one"}
    dic_new = {"key_one_dim_one" : "val_one_dim_one", "key_two_dim_one" : "val_two_dim_one", "key_three_dim_one" : "val_three_dim_one"}
    mdd_old = MultiDimDict(dic_old, 1)
    mdd_new = MultiDimDict(dic_new, 1)

    operations = mdd_new.get_operations(mdd_old)

    assert isinstance(operations[0], OP_MDD_Insert)
    assert operations[0].path == []
    assert operations[0].value == {"key_two_dim_one" : "val_two_dim_one"}

    assert isinstance(operations[1], OP_MDD_Insert)
    assert operations[1].path == []
    assert operations[1].value == {"key_three_dim_one" : "val_three_dim_one"}

def test_get_operations_insert_dim_two():
    dic_old = {"key_one_dim_one" : {"key_one_dim_two" : "val_one_dim_two"}}
    dic_new = {"key_one_dim_one" : {"key_one_dim_two" : "val_one_dim_two", "key_two_dim_two" : "val_two_dim_two"}}
    mdd_old = MultiDimDict(dic_old, 1)
    mdd_new = MultiDimDict(dic_new, 2)

    operations = mdd_new.get_operations(mdd_old)

    assert isinstance(operations[0], OP_MDD_Insert)
    assert operations[0].path == ["key_one_dim_one"]
    assert operations[0].value == {"key_two_dim_two" : "val_two_dim_two"}

def test_get_operations_insert_multiple_dims():
    dic_old = {"key_one_dim_one" : {"key_one_dim_two" : "val_one_dim_two"}}
    dic_new = {"key_one_dim_one" : {"key_one_dim_two" : "val_one_dim_two", "key_two_dim_two" : {"key_one_dim_three" : "val_one_dim_three"}}}
    mdd_old = MultiDimDict(dic_old, 1)
    mdd_new = MultiDimDict(dic_new, 2)

    operations = mdd_new.get_operations(mdd_old)

    assert isinstance(operations[0], OP_MDD_Insert)
    assert operations[0].path == ["key_one_dim_one"]
    assert operations[0].value == {"key_two_dim_two" : {"key_one_dim_three" : "val_one_dim_three"}}

def test_get_operations_single_remove():
    dic_new = {"key_one_dim_one" : "val_one_dim_one"}
    dic_old = {"key_one_dim_one" : "val_one_dim_one", "key_two_dim_one" : "val_two_dim_one"}
    mdd_old = MultiDimDict(dic_old, 1)
    mdd_new = MultiDimDict(dic_new, 1)

    operations = mdd_new.get_operations(mdd_old)

    assert isinstance(operations[0], OP_MDD_Remove)
    assert operations[0].path == ["key_two_dim_one"]
    assert operations[0].value == {"key_two_dim_one" : "val_two_dim_one"}


def test_get_operations_two_removes():
    dic_new = {"key_one_dim_one" : "val_one_dim_one"}
    dic_old = {"key_one_dim_one" : "val_one_dim_one", "key_two_dim_one" : "val_two_dim_one", "key_three_dim_one" : "val_three_dim_one"}
    mdd_old = MultiDimDict(dic_old, 1)
    mdd_new = MultiDimDict(dic_new, 1)

    operations = mdd_new.get_operations(mdd_old)

    assert isinstance(operations[0], OP_MDD_Remove)
    print(operations[0].path)
    assert operations[0].path == ["key_two_dim_one"]
    assert operations[0].value == {"key_two_dim_one" : "val_two_dim_one"}

    assert isinstance(operations[1], OP_MDD_Remove)
    print(operations[1].path)
    assert operations[1].path == ["key_three_dim_one"]
    assert operations[1].value == {"key_three_dim_one" : "val_three_dim_one"}

def test_get_operations_remove_dim_two():
    dic_new = {"key_one_dim_one" : {"key_two_dim_two" : "val_two_dim_two"}}
    dic_old = {"key_one_dim_one" : {"key_one_dim_two" : "val_one_dim_two", "key_two_dim_two" : "val_two_dim_two"}}
    mdd_old = MultiDimDict(dic_old, 2)
    mdd_new = MultiDimDict(dic_new, 1)

    operations = mdd_new.get_operations(mdd_old)

    assert isinstance(operations[0], OP_MDD_Remove)
    assert operations[0].path == ["key_one_dim_one", "key_one_dim_two"]
    assert operations[0].value == {"key_one_dim_two" : "val_one_dim_two"}


def test_get_operations_single_change():
    dic_new = {"key_one_dim_one" : "A"}
    dic_old = {"key_one_dim_one" : "B"}
    mdd_new = MultiDimDict(dic_new, 1)
    mdd_old = MultiDimDict(dic_old, 1)

    operations = mdd_new.get_operations(mdd_old)

    assert isinstance(operations[0], OP_MDD_Change)
    assert operations[0].path == ["key_one_dim_one"]
    assert operations[0].old_value == "B"
    assert operations[0].new_value == "A"

def test_get_operations_multiple_changes():
    dic_new = {"key_one_dim_one" : "A", "key_two_dim_one" : "C"}
    dic_old = {"key_one_dim_one" : "B", "key_two_dim_one" : 'D'}
    mdd_new = MultiDimDict(dic_new, 1)
    mdd_old = MultiDimDict(dic_old, 1)

    operations = mdd_new.get_operations(mdd_old)

    assert isinstance(operations[0], OP_MDD_Change)
    print(operations[0].path)
    assert operations[0].path == ["key_one_dim_one"]
    assert operations[0].old_value == "B"
    assert operations[0].new_value == "A"

    assert isinstance(operations[1], OP_MDD_Change)
    assert operations[1].path == ["key_two_dim_one"]
    assert operations[1].old_value == "D"
    assert operations[1].new_value == "C"

def test_get_operations_change_dim_two():
    dic_new = {"key_one_dim_one" : {"key_one_dim_two" : "A", "key_two_dim_two" : 'C'}}
    dic_old = {"key_one_dim_one" : {"key_one_dim_two" : "B", "key_two_dim_two" : 'D'}}
    mdd_new = MultiDimDict(dic_new, 1)
    mdd_old = MultiDimDict(dic_old, 1)

    operations = mdd_new.get_operations(mdd_old)

    assert isinstance(operations[0], OP_MDD_Change)
    assert operations[0].path == ["key_one_dim_one", "key_one_dim_two"]
    assert operations[0].old_value == "B"
    assert operations[0].new_value == "A"

    assert isinstance(operations[1], OP_MDD_Change)
    assert operations[1].path == ["key_one_dim_one", "key_two_dim_two"]
    assert operations[1].old_value == "D"
    assert operations[1].new_value == "C"

def test_get_operations_insert_and_change():
    dic_new = {"key_one_dim_one" : {"key_one_dim_two" : "A"}, "key_two_dim_one" : "val_two_dim_one"}
    dic_old = {"key_one_dim_one" : {"key_one_dim_two" : "B"}}

    mdd_new = MultiDimDict(dic_new, 1)
    mdd_old = MultiDimDict(dic_old, 1)

    operations = mdd_new.get_operations(mdd_old)

    assert isinstance(operations[0], OP_MDD_Change)
    assert operations[0].path == ["key_one_dim_one", "key_one_dim_two"]
    assert operations[0].old_value == "B"
    assert operations[0].new_value == "A"

    assert isinstance(operations[1], OP_MDD_Insert)
    print(operations[1].path)
    print(operations[1].value)
    assert operations[1].path == []
    assert operations[1].value == {"key_two_dim_one" : "val_two_dim_one"}



def test_get_operations_insert_and_remove_and_change():
    dic_new = {"key_one_dim_one" : {"key_one_dim_two" : "A"}, "key_two_dim_one" : "val_two_dim_one"}
    dic_old = {"key_one_dim_one" : {"key_one_dim_two" : "B", "key_two_dim_two" : "val_two_dim_two"}}

    mdd_new = MultiDimDict(dic_new, 1)
    mdd_old = MultiDimDict(dic_old, 1)

    operations = mdd_new.get_operations(mdd_old)

    assert isinstance(operations[0], OP_MDD_Change)
    assert operations[0].path == ["key_one_dim_one", "key_one_dim_two"]
    assert operations[0].old_value == "B"
    assert operations[0].new_value == "A"

    assert isinstance(operations[1], OP_MDD_Remove)
    assert operations[1].path == ["key_one_dim_one", "key_two_dim_two"]
    assert operations[1].value == {"key_two_dim_two" : "val_two_dim_two"}

    assert isinstance(operations[2], OP_MDD_Insert)
    print(operations[2].path)
    print(operations[2].value)
    assert operations[2].path == []
    assert operations[2].value == {"key_two_dim_one" : "val_two_dim_one"}


    

    

