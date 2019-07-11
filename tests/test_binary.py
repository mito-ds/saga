import pytest
from version_control.file_types.file.FileOpAdd import FileOpAdd
from version_control.file_types.binary_file.BinaryFile import BinaryFile
from version_control.file_types.binary_file.BinaryOpChangeContents import BinaryOpChangeContents
from version_control.Patch import Patch
from version_control.Branch import Branch


def test_add():
    branch = Branch()
    binary_file = BinaryFile("filename", "")
    addOp = FileOpAdd("filename", binary_file)
    patch = Patch([addOp])
    branch.add_patch(patch)

    assert len(branch.states[-1].files) == 1
    assert branch.states[-1].files["filename"] == binary_file

def test_change_contents():
    branch = Branch()
    binary_file = BinaryFile("filename", "")
    addOp = FileOpAdd("filename", binary_file)
    patch = Patch([addOp])
    branch.add_patch(patch)

    changeOp = BinaryOpChangeContents("filename", "new_data")
    patch = Patch([changeOp])
    branch.add_patch(patch)

    assert len(branch.states[-1].files) == 1
    assert branch.states[-1].files["filename"].file_contents == "new_data"
