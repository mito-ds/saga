import pytest
from version_control.file_types.file.FileOpAdd import FileOpAdd
from version_control.file_types.file.FileOpRemove import FileOpRemove
from version_control.Patch import Patch
from version_control.Branch import Branch

def test_add():
    branch = Branch()
    addOp = FileOpAdd("filename", "DATA")
    patch = Patch(set([addOp]))
    branch.add_patch(patch)

    assert len(branch.states[-1].files) == 1
    assert branch.states[-1].files["filename"] == "DATA"

def test_add_twice_fails():
    branch = Branch()
    addOp1 = FileOpAdd("filename", "DATA")
    addOp2 = FileOpAdd("filename", "DATA1")
    patch = Patch([addOp1, addOp2])
    with pytest.raises(Exception):
        branch.add_patch(patch)

def test_remove():
    branch = Branch()
    addOp = FileOpAdd("filename", "DATA")
    patch = Patch([addOp])
    branch.add_patch(patch)

    removeOp = FileOpRemove("filename")
    patch = Patch([removeOp])
    branch.add_patch(patch)

def test_remove_not_exist_fails():
    branch = Branch()
    removeOp = FileOpRemove("filename")
    patch = Patch([removeOp])
    with pytest.raises(Exception):
        branch.add_patch(patch)
