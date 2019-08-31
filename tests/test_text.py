import pytest
import os
from version_control.file_types.file.FileOpInsert import FileOpInsert
from version_control.file_types.text_file.TextFile import TextFile
from version_control.file_types.text_file.TextOpInsertLine import TextOpInsertLine
from version_control.file_types.text_file.TextOpRemoveLine import TextOpRemoveLine
from version_control.Patch import Patch
from version_control.Branch import Branch


def test_insert():
    branch = Branch()
    text_file = TextFile("filename", [""])
    insertOp = FileOpInsert("filename", text_file)
    patch = Patch([insertOp])
    branch.insert_patch(patch)

    assert len(branch.states[-1].files) == 1
    assert branch.states[-1].files["filename"] == text_file


def test_insert_line():
    branch = Branch()
    text_file = TextFile("filename", ["", ""])
    insertOp = FileOpInsert("filename", text_file)
    patch = Patch([insertOp])
    branch.insert_patch(patch)

    appendOp = TextOpInsertLine("filename", 1, "new_line")
    patch = Patch([appendOp])
    branch.insert_patch(patch)

    assert len(branch.states[-1].files["filename"].file_contents) == 3
    assert branch.states[-1].files["filename"].file_contents[1] == "new_line"



def test_remove_line():
    branch = Branch()
    text_file = TextFile("filename", ["new_line"])
    insertOp = FileOpInsert("filename", text_file)
    patch = Patch([insertOp])
    branch.insert_patch(patch)

    appendOp = TextOpRemoveLine("filename", 0)
    patch = Patch([appendOp])
    branch.insert_patch(patch)

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


def test_get_operations_remove_line():
    text_file1 = TextFile("filename", ["123"])
    text_file2 = TextFile("filename", [])
    operations = text_file1.get_operations(text_file2)
    assert len(operations) == 1
    assert isinstance(operations[0], TextOpRemoveLine)
    assert operations[0].file_name == "filename"
    assert operations[0].line_number == 0

def test_get_operations_remove_insert_line():
    text_file1 = TextFile("filename", [""])
    text_file2 = TextFile("filename", ["123"])
    operations = text_file1.get_operations(text_file2)
    assert len(operations) == 2
    assert isinstance(operations[0], TextOpRemoveLine)
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
    assert isinstance(operations[0], TextOpRemoveLine)
    assert operations[0].file_name == "filename"
    assert operations[0].line_number == 3
    assert isinstance(operations[1], TextOpRemoveLine)
    assert operations[1].file_name == "filename"
    assert operations[1].line_number == 2
    assert isinstance(operations[2], TextOpInsertLine)
    assert operations[2].file_name == "filename"
    assert operations[2].line_number == 1
    assert operations[2].line_contents == "k"

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

def test_to_from_string_remove():
    remove_op = TextOpRemoveLine("binary", 0)
    remove_op_string = remove_op.to_string()
    remove_op1 = TextOpRemoveLine.from_string(remove_op_string)
    assert remove_op.file_name == remove_op1.file_name
    assert remove_op.line_number == remove_op1.line_number

def test_to_from_file():
    text_file = TextFile(os.getcwd() + "/temp/text", ["hi", "yo"])
    text_file.to_file(os.getcwd() + "/temp/text")
    text_file1 = TextFile.from_file(os.getcwd() + "/temp/text")
    assert text_file1.file_name == os.getcwd() + "/temp/text"
    assert text_file1.file_contents == ["hi", "yo"]


"""
def test_edit_difference_match():
    list1 = ["def"]
    list2 = ["HAHAHA", "defi"]
    lcs_indexes_old, lcs_indexes_new = lcs_close(list1, list2)
    assert lcs_indexes_old[0] == 0
    assert lcs_indexes_new[0] == 1


def test_edit_difference_match_large():

    list1 = [
        "for (int i = 0; i < 100; i++ ) {",
        "System.out.println(i * 2);",
        "int temp = i * 1000;",
        "if (temp < i) {",
        "System.out.println(temp, i);",
        "}",
        "}",
    ]
    list2 = [
        "for (int j = 0; j < 100; j++ ) {",
        "int temp1 = j * 1000;",
        "if (temp1 < j) {",
        "System.out.println(temp1, j);",
        "}",
        "}",
    ]

    lcs_indexes_old, lcs_indexes_new = lcs_close(list1, list2)
    assert len(lcs_indexes_old) == 6
    assert lcs_indexes_old == [0, 2, 3, 4, 5, 6]
    assert lcs_indexes_new == [0, 1, 2, 3, 4, 5]
"""