import pytest
import os
import json
from version_control.file_types.json_file.JSONOpListDelete import JSONOpListDelete
from version_control.file_types.json_file.JSONOpListInsert import JSONOpListInsert
from version_control.file_types.json_file.JSONOpDictAdd import JSONOpDictAdd
from version_control.file_types.json_file.JSONOpDictDelete import JSONOpDictDelete
from version_control.file_types.json_file.JSONOpPrimitiveChange import JSONOpPrimitiveChange
from version_control.file_types.json_file.JSONFile import JSONFile
from version_control.file_types.file.FileOpAdd import FileOpAdd
from version_control.Patch import Patch
from version_control.Branch import Branch


def test_create():
    branch = Branch()
    json_file = JSONFile("filename", dict())
    add_op = FileOpAdd("filename", json_file)
    patch = Patch([add_op])
    branch.add_patch(patch)

    assert len(branch.states[-1].files) == 1
    assert branch.states[-1].files["filename"] == json_file


def test_add_dict():
    branch = Branch()
    json_file = JSONFile("filename", {})
    add_op = FileOpAdd("filename", json_file)
    add_dict_op = JSONOpDictAdd("filename", ["key"], 123)
    patch = Patch([add_op, add_dict_op])
    branch.add_patch(patch)

    assert len(branch.states[-1].files) == 1
    assert len(branch.states[-1].files["filename"].file_contents) == 1
    assert branch.states[-1].files["filename"].file_contents['key'] == 123

def test_remove_dict():
    branch = Branch()
    json_file = JSONFile("filename", {'key': 123})
    add_op = FileOpAdd("filename", json_file)
    del_dict_op = JSONOpDictDelete("filename", ["key"])
    patch = Patch([add_op, del_dict_op])
    branch.add_patch(patch)

    assert len(branch.states[-1].files) == 1
    assert len(branch.states[-1].files["filename"].file_contents) == 0

def test_primitive_change():
    branch = Branch()
    json_file = JSONFile("filename", {'key': 123})
    add_op = FileOpAdd("filename", json_file)
    op = JSONOpPrimitiveChange("filename", ["key"], 124)
    patch = Patch([add_op, op])
    branch.add_patch(patch)

    assert len(branch.states[-1].files) == 1
    assert len(branch.states[-1].files["filename"].file_contents) == 1
    assert branch.states[-1].files["filename"].file_contents['key'] == 124

def test_list_delete():
    branch = Branch()
    json_file = JSONFile("filename", [1])
    add_op = FileOpAdd("filename", json_file)
    op = JSONOpListDelete("filename", ["0"])
    patch = Patch([add_op, op])
    branch.add_patch(patch)

    assert len(branch.states[-1].files) == 1
    assert len(branch.states[-1].files["filename"].file_contents) == 0

def test_list_insert():
    branch = Branch()
    json_file = JSONFile("filename", [1])
    add_op = FileOpAdd("filename", json_file)
    op = JSONOpListInsert("filename", ["1"], 2)
    patch = Patch([add_op, op])
    branch.add_patch(patch)

    assert len(branch.states[-1].files) == 1
    assert len(branch.states[-1].files["filename"].file_contents) == 2
    assert branch.states[-1].files["filename"].file_contents[0] == 1
    assert branch.states[-1].files["filename"].file_contents[1] == 2

def test_get_operations():
    json_file1 = JSONFile("filename", dict())
    json_file2 = JSONFile("filename", {"key": 123})

    operations = json_file1.get_operations(json_file2)
    assert len(operations) == 1
    assert isinstance(operations[0], JSONOpDictAdd)
    assert len(operations[0].path) == 1
    assert operations[0].path[0] == "key"
    assert operations[0].new_value == 123


def test_get_operations_list():
    json_file1 = JSONFile("filename", {"list": ["a", "b", "c", "d", "e"]})
    json_file2 = JSONFile("filename", {"list": ["a", "k", "b", "e"]})
    operations = json_file1.get_operations(json_file2)
    assert len(operations) == 3
    assert isinstance(operations[0], JSONOpListInsert)
    assert operations[0].file_name == "filename"
    assert operations[0].path[1] == "1"
    assert operations[0].new_value == "k"
    assert isinstance(operations[1], JSONOpListDelete)
    assert operations[1].file_name == "filename"
    assert operations[1].path[1] == "3"
    assert isinstance(operations[2], JSONOpListDelete)
    assert operations[2].file_name == "filename"
    assert operations[2].path[1] == "3"

def test_get_operations_complex_object():
    json_file1 = JSONFile("filename", {"list": ["a", "b", "c", "d", "e"], "obj": {"key": 122}})
    json_file2 = JSONFile("filename", {"list": ["a", "k", "b", "e"], "obj": {"key": 123}})
    operations = json_file1.get_operations(json_file2)
    assert len(operations) == 4
    assert isinstance(operations[0], JSONOpListInsert)
    assert operations[0].file_name == "filename"
    assert operations[0].path[1] == "1"
    assert operations[0].new_value == "k"
    assert isinstance(operations[1], JSONOpListDelete)
    assert operations[1].file_name == "filename"
    assert operations[1].path[1] == "3"
    assert isinstance(operations[2], JSONOpListDelete)
    assert operations[2].file_name == "filename"
    assert operations[2].path[1] == "3"
    assert isinstance(operations[3], JSONOpPrimitiveChange)


def test_get_operations_disjoint_keys():
    json_file1 = JSONFile("filename", {"list1": ["a", "b", "c", "d", "e"]})
    json_file2 = JSONFile("filename", {"list2": ["a", "k", "b", "e"]})
    operations = json_file1.get_operations(json_file2)
    assert len(operations) == 2
    assert isinstance(operations[0], JSONOpDictDelete)
    assert operations[0].file_name == "filename"
    assert operations[0].path[0] == "list1"
    assert isinstance(operations[1], JSONOpDictAdd)
    assert operations[1].file_name == "filename"
    assert operations[1].path[0] == "list2"
    assert operations[1].new_value == ["a", "k", "b", "e"]
    # TODO: note, we might be able to do better just by doing a git line
    # diff, and seeing what results in bigger changes here. There's some heuristic...

