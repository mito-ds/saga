import pytest
import os
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

def test_get_operations_change():
    binary_file1 = BinaryFile("filename", "")
    binary_file2 = BinaryFile("filename", "stuff")
    operations = binary_file1.get_operations(binary_file2)
    assert len(operations) == 1
    assert operations[0].file_name == "filename"
    assert operations[0].file_contents == "stuff"

def test_get_operations_no_change():
    binary_file1 = BinaryFile("filename", "")
    binary_file2 = BinaryFile("filename", "")
    operations = binary_file1.get_operations(binary_file2)
    assert len(operations) == 0

def test_to_from_string():
    binary_file = BinaryFile("binary", "010101")
    binary_file_string = binary_file.to_string()
    binary_file1 = BinaryFile.from_string(binary_file_string)
    assert binary_file.file_name == binary_file1.file_name
    assert binary_file.file_contents == binary_file1.file_contents

def test_to_from_string_change():
    change_op = BinaryOpChangeContents("binary", "0101")
    change_op_string = change_op.to_string()
    change_op1 = BinaryOpChangeContents.from_string(change_op_string)
    assert change_op.file_name == change_op1.file_name
    assert change_op.file_contents == change_op1.file_contents

def test_to_from_file():
    binary_file = BinaryFile(os.getcwd() + "/temp/binary", "0101")
    binary_file.to_file(os.getcwd() + "/temp/binary")
    binary_file1 = BinaryFile.from_file(os.getcwd() + "/temp/binary")
    assert binary_file1.file_name == os.getcwd() + "/temp/binary"
    assert binary_file1.file_contents == "0101"

