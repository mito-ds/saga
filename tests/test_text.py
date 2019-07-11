import pytest
from version_control.file_types.file.FileOpAdd import FileOpAdd
from version_control.file_types.text_file.TextFile import TextFile
from version_control.file_types.text_file.TextOpChangeLine import TextOpChangeLine
from version_control.file_types.text_file.TextOpInsertLine import TextOpInsertLine
from version_control.file_types.text_file.TextOpDeleteLine import TextOpDeleteLine
from version_control.Patch import Patch
from version_control.Branch import Branch


def test_add():
    branch = Branch()
    text_file = TextFile("filename", [""])
    addOp = FileOpAdd("filename", text_file)
    patch = Patch([addOp])
    branch.add_patch(patch)

    assert len(branch.states[-1].files) == 1
    assert branch.states[-1].files["filename"] == text_file

def test_change_line():
    branch = Branch()
    text_file = TextFile("filename", [""])
    addOp = FileOpAdd("filename", text_file)
    patch = Patch([addOp])
    branch.add_patch(patch)

    appendOp = TextOpChangeLine("filename", 0, "new_line")
    patch = Patch([appendOp])
    branch.add_patch(patch)

    assert len(branch.states[-1].files["filename"].file_contents) == 1
    assert branch.states[-1].files["filename"].file_contents[0] == "new_line"


def test_insert_line():
    branch = Branch()
    text_file = TextFile("filename", ["", ""])
    addOp = FileOpAdd("filename", text_file)
    patch = Patch([addOp])
    branch.add_patch(patch)

    appendOp = TextOpInsertLine("filename", 1, "new_line")
    patch = Patch([appendOp])
    branch.add_patch(patch)

    assert len(branch.states[-1].files["filename"].file_contents) == 3
    assert branch.states[-1].files["filename"].file_contents[1] == "new_line"



def test_delete_line():
    branch = Branch()
    text_file = TextFile("filename", ["new_line"])
    addOp = FileOpAdd("filename", text_file)
    patch = Patch([addOp])
    branch.add_patch(patch)

    appendOp = TextOpDeleteLine("filename", 0)
    patch = Patch([appendOp])
    branch.add_patch(patch)

    assert len(branch.states[-1].files) == 1
    assert len(branch.states[-1].files["filename"].file_contents) == 0

def test_get_operations_same():
    text_file1 = TextFile("filename", [""])
    text_file2 = TextFile("filename", [""])
    operations = text_file1.get_operations(text_file2)
    assert len(operations) == 0

    text_file1 = TextFile("filename", ["hi", "i", "am", "nate"])
    text_file2 = TextFile("filename", ["hi", "i", "am", "nate"])
    operations = text_file1.get_operations(text_file2)
    assert len(operations) == 0


def test_get_operations_append_line():
    text_file1 = TextFile("filename", [""])
    text_file2 = TextFile("filename", ["123"])
    operations = text_file1.get_operations(text_file2)
    assert len(operations) == 0

    text_file1 = TextFile("filename", ["hi", "i", "am", "nate"])
    text_file2 = TextFile("filename", ["hi", "i", "am", "nate"])
    operations = text_file1.get_operations(text_file2)
    assert len(operations) == 0
