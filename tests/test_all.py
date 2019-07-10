import pytest
from version_control.operations.AddFileOperation import AddFileOperation
from version_control.operations.RemoveFileOperation import RemoveFileOperation
from version_control.Patch import Patch
from version_control.Branch import Branch

def test_add():
    branch = Branch()
    addOp = AddFileOperation("filename", "DATA")
    patch = Patch(set([addOp]))
    branch.add_patch(patch)

    assert len(branch.states[-1].files) == 1
    assert branch.states[-1].files["filename"] == "DATA"

def test_add_twice_fails():
    branch = Branch()
    addOp1 = AddFileOperation("filename", "DATA")
    addOp2 = AddFileOperation("filename", "DATA1")
    patch = Patch(set([addOp1, addOp2]))
    with pytest.raises(Exception):
        branch.add_patch(patch)

def test_remove():
    branch = Branch()
    addOp = AddFileOperation("filename", "DATA")
    patch = Patch(set([addOp]))
    branch.add_patch(patch)

    removeOp = RemoveFileOperation("filename")
    patch = Patch(set([removeOp]))
    branch.add_patch(patch)

def test_remove_not_exist_fails():
    branch = Branch()
    removeOp = RemoveFileOperation("filename")
    patch = Patch(set([removeOp]))
    with pytest.raises(Exception):
        branch.add_patch(patch)
