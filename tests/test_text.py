import pytest
import os
from version_control.file_types.file.FileOpAdd import FileOpAdd
from version_control.file_types.text_file.TextFile import TextFile
from version_control.file_types.text_file.TextOpInsertLine import TextOpInsertLine
from version_control.file_types.text_file.TextOpDeleteLine import TextOpDeleteLine
from version_control.file_types.text_file.TextOpChangeLine import TextOpChangeLine
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

def test_get_operations_change_line():
    text_file1 = TextFile("filename", [""])
    text_file2 = TextFile("filename", ["123"])
    operations = text_file1.get_operations(text_file2)
    assert len(operations) == 1
    assert isinstance(operations[0], TextOpChangeLine)
    assert operations[0].file_name == "filename"
    assert operations[0].line_number == 0
    assert operations[0].line_contents == "123"


def test_get_operations_complex_changes():
    text_file1 = TextFile("filename", ["a", "b", "c", "d", "e"])
    text_file2 = TextFile("filename", ["a", "k", "b", "e"])
    operations = text_file1.get_operations(text_file2)
    assert len(operations) == 3
    assert isinstance(operations[0], TextOpInsertLine)
    assert operations[0].file_name == "filename"
    assert operations[0].line_number == 1
    assert operations[0].line_contents == "k"
    assert isinstance(operations[1], TextOpDeleteLine)
    assert operations[1].file_name == "filename"
    assert operations[1].line_number == 3
    assert isinstance(operations[2], TextOpDeleteLine)
    assert operations[2].file_name == "filename"
    assert operations[2].line_number == 3

def test_to_from_string():
    text_file = TextFile("text", ["this", "is", "a", "file"])
    text_file_string = text_file.to_string()
    text_file1 = TextFile.from_string(text_file_string)
    assert text_file.file_name == text_file1.file_name 
    assert text_file.file_contents == text_file1.file_contents 

def test_to_from_string_insert():
    insert_op = TextOpInsertLine("binary", 0, "100")
    insert_op_string = insert_op.to_string()
    insert_op1 = TextOpInsertLine.from_string(insert_op_string)
    assert insert_op.file_name == insert_op1.file_name
    assert insert_op.line_number == insert_op1.line_number
    assert insert_op.line_contents == insert_op1.line_contents

def test_to_from_string_delete():
    delete_op = TextOpDeleteLine("binary", 0)
    delete_op_string = delete_op.to_string()
    delete_op1 = TextOpDeleteLine.from_string(delete_op_string)
    assert delete_op.file_name == delete_op1.file_name
    assert delete_op.line_number == delete_op1.line_number

def test_to_from_file():
    text_file = TextFile(os.getcwd() + "/temp/text", ["hi", "yo"])
    text_file.to_file(os.getcwd() + "/temp/text")
    text_file1 = TextFile.from_file(os.getcwd() + "/temp/text")
    assert text_file1.file_name == os.getcwd() + "/temp/text"
    assert text_file1.file_contents == ["hi", "yo"]