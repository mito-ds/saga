import pytest
from version_control.file_types.file.FileOpAdd import FileOpAdd
from version_control.file_types.file.FileOpRemove import FileOpRemove
from version_control.Patch import Patch
from version_control.Branch import Branch
from version_control.file_types.binary_file.BinaryFile import BinaryFile

def test_add():
    branch = Branch()
    add_op = FileOpAdd("filename", "DATA")
    patch = Patch(set([add_op]))
    branch.add_patch(patch)

    assert len(branch.states[-1].files) == 1
    assert branch.states[-1].files["filename"] == "DATA"

def test_add_twice_fails():
    branch = Branch()
    add_op1 = FileOpAdd("filename", "DATA")
    add_op2 = FileOpAdd("filename", "DATA1")
    patch = Patch([add_op1, add_op2])
    with pytest.raises(Exception):
        branch.add_patch(patch)

def test_remove():
    branch = Branch()
    add_op = FileOpAdd("filename", "DATA")
    patch = Patch([add_op])
    branch.add_patch(patch)

    remove_op = FileOpRemove("filename")
    patch = Patch([remove_op])
    branch.add_patch(patch)

def test_remove_not_exist_fails():
    branch = Branch()
    remove_op = FileOpRemove("filename")
    patch = Patch([remove_op])
    with pytest.raises(Exception):
        branch.add_patch(patch)

def test_to_from_string_add_file():
    binary_file = BinaryFile("binary", "0101")
    add_op = FileOpAdd("binary", binary_file)
    add_op_string = add_op.to_string()
    add_op1 = FileOpAdd.from_string(add_op_string)
    assert add_op.file_name == add_op1.file_name
    assert add_op.file.file_name == add_op1.file.file_name
    assert add_op.file.file_contents == add_op1.file.file_contents

def test_to_from_string_remove_file():
    remove_op = FileOpRemove("binary")
    remove_op_string = remove_op.to_string()
    remove_op1 = FileOpRemove.from_string(remove_op_string)
    assert remove_op.file_name == remove_op1.file_name


