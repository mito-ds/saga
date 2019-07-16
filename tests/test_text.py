import pytest
import os
from version_control.file_types.file.FileOpAdd import FileOpAdd
from version_control.file_types.text_file.TextFile import TextFile
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


def test_get_operations_insert_line():
    text_file1 = TextFile("filename", [])
    text_file2 = TextFile("filename", ["123"])
    operations = text_file1.get_operations(text_file2)
    assert len(operations) == 1
    assert isinstance(operations[0], TextOpInsertLine)
    assert operations[0].file_name == "filename"
    assert operations[0].line_number == 0
    assert operations[0].line_contents == "123"


def test_get_operations_delete_line():
    text_file1 = TextFile("filename", ["123"])
    text_file2 = TextFile("filename", [])
    operations = text_file1.get_operations(text_file2)
    assert len(operations) == 1
    assert isinstance(operations[0], TextOpDeleteLine)
    assert operations[0].file_name == "filename"
    assert operations[0].line_number == 0

def test_get_operations_delete_insert_line():
    text_file1 = TextFile("filename", [""])
    text_file2 = TextFile("filename", ["123"])
    operations = text_file1.get_operations(text_file2)
    assert len(operations) == 2
    assert isinstance(operations[0], TextOpDeleteLine)
    assert operations[0].file_name == "filename"
    assert operations[0].line_number == 0
    assert isinstance(operations[1], TextOpInsertLine)
    assert operations[1].file_name == "filename"
    assert operations[1].line_number == 0
    assert operations[1].line_contents == "123"


def test_get_operations_complex_changes():
    text_file1 = TextFile("filename", ["a", "b", "c", "d", "e"])
    text_file2 = TextFile("filename", ["a", "k", "b", "e"])
    operations = text_file1.get_operations(text_file2)
    assert len(operations) == 3
    assert isinstance(operations[0], TextOpDeleteLine)
    assert operations[0].file_name == "filename"
    assert operations[0].line_number == 2
    assert isinstance(operations[1], TextOpDeleteLine)
    assert operations[1].file_name == "filename"
    assert operations[1].line_number == 2
    assert isinstance(operations[2], TextOpInsertLine)
    assert operations[2].file_name == "filename"
    assert operations[2].line_number == 1
    assert operations[2].line_contents == "k"

def test_read_write_file():
    text_file = TextFile(os.getcwd() + "/temp/text", ["this", "is", "a", "file"])
    text_file.write_file()
    text_file1 = TextFile.read_file(os.getcwd() + "/temp/text")
    assert "".join(text_file1.file_contents) == "this\nis\na\nfile\n"