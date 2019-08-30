import pytest
from version_control.file_types.file.FileOpInsert import FileOpInsert
from version_control.file_types.file.FileOpRemove import FileOpRemove
from version_control.Patch import Patch
from version_control.Branch import Branch
from version_control.file_types.binary_file.BinaryFile import BinaryFile

def test_insert():
    branch = Branch()
    insert_op = FileOpInsert("filename", "DATA")
    patch = Patch(set([insert_op]))
    branch.insert_patch(patch)

    assert len(branch.states[-1].files) == 1
    assert branch.states[-1].files["filename"] == "DATA"

def test_insert_twice_fails():
    branch = Branch()
    insert_op1 = FileOpInsert("filename", "DATA")
    insert_op2 = FileOpInsert("filename", "DATA1")
    patch = Patch([insert_op1, insert_op2])
    with pytest.raises(Exception):
        branch.insert_patch(patch)

def test_remove():
    branch = Branch()
    insert_op = FileOpInsert("filename", "DATA")
    patch = Patch([insert_op])
    branch.insert_patch(patch)

    remove_op = FileOpRemove("filename")
    patch = Patch([remove_op])
    branch.insert_patch(patch)

def test_remove_not_exist_fails():
    branch = Branch()
    remove_op = FileOpRemove("filename")
    patch = Patch([remove_op])
    with pytest.raises(Exception):
        branch.insert_patch(patch)

def test_to_from_string_insert_file():
    binary_file = BinaryFile("binary", "0101")
    insert_op = FileOpInsert("binary", binary_file)
    insert_op_string = insert_op.to_string()
    insert_op1 = FileOpInsert.from_string(insert_op_string)
    assert insert_op.file_name == insert_op1.file_name
    assert insert_op.file.file_name == insert_op1.file.file_name
    assert insert_op.file.file_contents == insert_op1.file.file_contents

def test_to_from_string_remove_file():
    remove_op = FileOpRemove("binary")
    remove_op_string = remove_op.to_string()
    remove_op1 = FileOpRemove.from_string(remove_op_string)
    assert remove_op.file_name == remove_op1.file_name


