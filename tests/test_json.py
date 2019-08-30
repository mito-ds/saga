import pytest
import os
import json
from version_control.file_types.json_file.JSONOpListRemove import JSONOpListRemove
from version_control.file_types.json_file.JSONOpListInsert import JSONOpListInsert
from version_control.file_types.json_file.JSONOpDictInsert import JSONOpDictInsert
from version_control.file_types.json_file.JSONOpDictRemove import JSONOpDictRemove
from version_control.file_types.json_file.JSONOpPrimitiveChange import JSONOpPrimitiveChange
from version_control.file_types.json_file.JSONFile import JSONFile
from version_control.file_types.file.FileOpInsert import FileOpInsert
from version_control.Patch import Patch
from version_control.Branch import Branch


def test_create():
    branch = Branch()
    json_file = JSONFile("filename", dict())
    insert_op = FileOpInsert("filename", json_file)
    patch = Patch([insert_op])
    branch.insert_patch(patch)

    assert len(branch.states[-1].files) == 1
    assert branch.states[-1].files["filename"] == json_file


def test_insert_dict():
    branch = Branch()
    json_file = JSONFile("filename", {})
    insert_op = FileOpInsert("filename", json_file)
    insert_dict_op = JSONOpDictInsert("filename", ["key"], 123)
    patch = Patch([insert_op, insert_dict_op])
    branch.insert_patch(patch)

    assert len(branch.states[-1].files) == 1
    assert len(branch.states[-1].files["filename"].file_contents) == 1
    assert branch.states[-1].files["filename"].file_contents['key'] == 123

def test_remove_dict():
    branch = Branch()
    json_file = JSONFile("filename", {'key': 123})
    insert_op = FileOpInsert("filename", json_file)
    del_dict_op = JSONOpDictRemove("filename", ["key"])
    patch = Patch([insert_op, del_dict_op])
    branch.insert_patch(patch)

    assert len(branch.states[-1].files) == 1
    assert len(branch.states[-1].files["filename"].file_contents) == 0

def test_primitive_change():
    branch = Branch()
    json_file = JSONFile("filename", {'key': 123})
    insert_op = FileOpInsert("filename", json_file)
    op = JSONOpPrimitiveChange("filename", ["key"], 124)
    patch = Patch([insert_op, op])
    branch.insert_patch(patch)

    assert len(branch.states[-1].files) == 1
    assert len(branch.states[-1].files["filename"].file_contents) == 1
    assert branch.states[-1].files["filename"].file_contents['key'] == 124

def test_list_remove():
    branch = Branch()
    json_file = JSONFile("filename", [1])
    insert_op = FileOpInsert("filename", json_file)
    op = JSONOpListRemove("filename", ["0"])
    patch = Patch([insert_op, op])
    branch.insert_patch(patch)

    assert len(branch.states[-1].files) == 1
    assert len(branch.states[-1].files["filename"].file_contents) == 0

def test_list_insert():
    branch = Branch()
    json_file = JSONFile("filename", [1])
    insert_op = FileOpInsert("filename", json_file)
    op = JSONOpListInsert("filename", ["1"], 2)
    patch = Patch([insert_op, op])
    branch.insert_patch(patch)

    assert len(branch.states[-1].files) == 1
    assert len(branch.states[-1].files["filename"].file_contents) == 2
    assert branch.states[-1].files["filename"].file_contents[0] == 1
    assert branch.states[-1].files["filename"].file_contents[1] == 2

def test_get_operations():
    json_file1 = JSONFile("filename", dict())
    json_file2 = JSONFile("filename", {"key": 123})

    operations = json_file1.get_operations(json_file2)
    assert len(operations) == 1
    assert isinstance(operations[0], JSONOpDictInsert)
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
    assert isinstance(operations[1], JSONOpListRemove)
    assert operations[1].file_name == "filename"
    assert operations[1].path[1] == "3"
    assert isinstance(operations[2], JSONOpListRemove)
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
    assert isinstance(operations[1], JSONOpListRemove)
    assert operations[1].file_name == "filename"
    assert operations[1].path[1] == "3"
    assert isinstance(operations[2], JSONOpListRemove)
    assert operations[2].file_name == "filename"
    assert operations[2].path[1] == "3"
    assert isinstance(operations[3], JSONOpPrimitiveChange)


def test_get_operations_disjoint_keys():
    json_file1 = JSONFile("filename", {"list1": ["a", "b", "c", "d", "e"]})
    json_file2 = JSONFile("filename", {"list2": ["a", "k", "b", "e"]})
    operations = json_file1.get_operations(json_file2)
    assert len(operations) == 2
    assert isinstance(operations[0], JSONOpDictRemove)
    assert operations[0].file_name == "filename"
    assert operations[0].path[0] == "list1"
    assert isinstance(operations[1], JSONOpDictInsert)
    assert operations[1].file_name == "filename"
    assert operations[1].path[0] == "list2"
    assert operations[1].new_value == ["a", "k", "b", "e"]
    # TODO: note, we might be able to do better just by doing a git line
    # diff, and seeing what results in bigger changes here. There's some heuristic..
    # sounds like a future research problem!

