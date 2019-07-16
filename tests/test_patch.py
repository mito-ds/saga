import pytest
from version_control.file_types.file.FileOpAdd import FileOpAdd
from version_control.file_types.file.FileOpRemove import FileOpRemove
from version_control.file_types.text_file.TextFile import TextFile
from version_control.file_types.text_file.TextOpInsertLine import TextOpInsertLine
from version_control.file_types.text_file.TextOpDeleteLine import TextOpDeleteLine
from version_control.Patch import Patch
from version_control.Branch import Branch


def test_patch_to_from_string():
    text_file = TextFile("filename", [""])
    addOp = FileOpAdd("filename", text_file)
    remove_op = FileOpRemove("filename")
    patch = Patch([addOp, remove_op])

    patch_string = patch.to_string()
    patch1 = Patch.from_string(patch_string)

    assert len(patch.operations) == len(patch1.operations) 
    assert patch.operations[0].file_name == patch1.operations[0].file_name
    assert patch.operations[0].file.file_contents == patch1.operations[0].file.file_contents
    assert patch.operations[1].file_name == patch1.operations[0].file_name
    assert isinstance(patch1.operations[0], FileOpAdd)
    assert isinstance(patch1.operations[1], FileOpRemove)