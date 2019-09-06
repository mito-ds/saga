import pytest
from saga.Patch import Patch
from saga.Branch import Branch
from saga.base_file.File import File
from saga.base_file.OP_File_Insert import OP_File_Insert
from saga.base_file.OP_File_Remove import OP_File_Remove
from saga.base_file.OP_File_ChangeName import OP_File_ChangeName

def blank_insert():
    return OP_File_Insert("id", "type", "name", "contents")

def blank_remove():
    return OP_File_Remove("id", "type", "name", "contents")

def test_insert():
    branch = Branch()
    insert_op = blank_insert()
    patch = Patch(set([insert_op]))
    branch.insert_patch(patch)

    assert len(branch.curr_state) == 1
    assert isinstance(branch.curr_state["id"], File)

def test_insert_twice_fails():
    branch = Branch()
    insert_op1 = blank_insert()
    insert_op2 = blank_insert()
    patch = Patch([insert_op1, insert_op2])
    with pytest.raises(Exception):
        branch.insert_patch(patch)

def test_remove():
    branch = Branch()
    insert_op = blank_insert()
    patch = Patch([insert_op])
    branch.insert_patch(patch)

    remove_op = blank_remove()
    patch = Patch([remove_op])
    branch.insert_patch(patch)

def test_remove_not_exist_fails():
    branch = Branch()
    remove_op = blank_remove()
    patch = Patch([remove_op, remove_op])
    with pytest.raises(Exception):
        branch.insert_patch(patch)