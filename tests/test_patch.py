import pytest
from saga.Patch import Patch
from saga.base_file.File import File
from saga.State import State 
from saga.data_types.multi_dim_list.MultiDimList import MultiDimList


def test_to_from_string_empty():
    patch = Patch([])
    s = patch.to_string()
    new_patch = patch.from_string(s)
    assert new_patch.operations == []

def test_to_from_string_operations():
    mdl1 = MultiDimList([1, 3, 5], 1)
    mdl2 = MultiDimList([1, 3, 2, 4], 1)
    ops = mdl1.get_operations(mdl2)
    patch = Patch(ops)
    s = patch.to_string()
    new_patch = patch.from_string(s)
    assert len(new_patch.operations) == len(patch.operations)


def test_two_patches_same_strings():
    mdl11 = MultiDimList([1, 3, 5], 1)
    mdl12 = MultiDimList([1, 3, 2, 4], 1)
    ops1 = mdl11.get_operations(mdl12)
    patch1 = Patch(ops1)
    mdl21 = MultiDimList([1, 3, 5], 1)
    mdl22 = MultiDimList([1, 3, 2, 4], 1)
    ops2 = mdl21.get_operations(mdl22)
    patch2 = Patch(ops2)
    assert patch1.to_string() == patch2.to_string()
    assert patch1.get_hash() == patch2.get_hash()
    

def test_applies_ops_correctly():
    mdl1 = MultiDimList([1, 3, 5], 1)
    mdl2 = MultiDimList([1, 3, 2, 4], 1)
    ops = mdl1.get_operations(mdl2)
    patch = Patch(ops)
    state1 = State({"id": File("id", "type", "name", mdl1)}, None)
    state2 = patch.apply_patch(state1)
    print(state2)
    assert state2["id"].file_contents.multi_dim_list == [1, 3, 2, 4]
    assert state2.prev_state_hash == state1.get_hash()