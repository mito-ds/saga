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

def test_read_write_file():
    binary_file = BinaryFile(os.getcwd() + "/temp/binary", "010101")
    binary_file.write_file()
    binary_file1 = BinaryFile.read_file(os.getcwd() + "/temp/binary")
    assert str(binary_file1.file_contents) == str(b"010101")
