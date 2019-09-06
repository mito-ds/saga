from saga.data_types.multi_dim_dict.multi_dim_dict import MultiDimDict
from saga.data_types.multi_dim_dict.OP_MDD_Change import OP_MDD_Change
from saga.data_types.multi_dim_dict.OP_MDD_Insert import OP_MDD_Insert
from saga.data_types.multi_dim_dict.OP_MDD_Remove import OP_MDD_Remove

def get_ops(dictonary1, dictonary2):
    mdd1 = MultiDimDict(dictonary1)
    mdd2 = MultiDimDict(dictonary2)
    return mdd1.get_operations(mdd2)

def test_no_changes_empty():
    ops = get_ops(dict(), dict())
    assert len(ops) == 0

def test_single_change():
    ops = get_ops({1: 2}, {1: 3})
    assert len(ops) == 1
    assert isinstance(ops[0], OP_MDD_Change)
    assert ops[0].path == [1]
    assert ops[0].old_value == 2
    assert ops[0].new_value == 3
    
def test_single_add():
    ops = get_ops({}, {1: 3})
    assert len(ops) == 1
    assert isinstance(ops[0], OP_MDD_Insert)
    assert ops[0].path == [1]
    assert ops[0].value == 3

def test_single_delete():
    ops = get_ops({1: 3}, {})
    assert len(ops) == 1
    assert isinstance(ops[0], OP_MDD_Remove)
    assert ops[0].path == [1]
    assert ops[0].value == 3

def test_nested_change():
    ops = get_ops({1: {1: 3}}, {})
    assert len(ops) == 1
    assert isinstance(ops[0], OP_MDD_Remove)
    assert ops[0].path == [1]
    assert ops[0].value == 3

