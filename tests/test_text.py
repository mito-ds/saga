import pytest
import os
from saga.base_file.File import File
from saga.file_types.text_file import parse_text_file, write_text_file

def create_text_file(name, contents):
    if os.path.isfile(name):
        os.remove(name)
    f = open(name, 'w+')
    f.write(contents)
    f.close()

@pytest.fixture()
def setup_text_files():
    if not os.path.isdir("temp"):
        os.mkdir('temp')
    create_text_file("temp/text0", "line1\nline2")

def test_create(setup_text_files):
    text_file = parse_text_file("id", "name", "temp/text0")
    assert text_file.file_name == "name"
    assert text_file.file_contents.mixed_data_type == ["line1", "line2"]

def test_create_then_write(setup_text_files):
    text_file = parse_text_file("id", "name", "temp/text0")
    write_text_file(text_file)
    f = open('temp/text0', 'r')
    assert f.read() == "line1\nline2"

def test_get_operations_no_change(setup_text_files):
    text_file0 = parse_text_file("id", "name", "temp/text0")
    text_file1 = parse_text_file("id", "name", "temp/text0")
    ops = text_file0.get_operations(text_file1)
    assert len(ops) == 0
    
def test_get_operations_insert_end(setup_text_files):
    text_file0 = parse_text_file("id", "name", "temp/text0")
    create_text_file("temp/text0", "line1\nline2\nline3")
    text_file1 = parse_text_file("id", "name", "temp/text0")
    ops = text_file0.get_operations(text_file1)
    assert len(ops) == 1
    assert isinstance(ops[0], OP_MDL_Insert)
    assert ops[0].path == [2]
    assert ops[0].value == ["line3"]

def test_get_operations_insert_middle(setup_text_files):
    text_file0 = parse_text_file("id", "name", "temp/text0")
    create_text_file("temp/text0", "line1\nline3\nline2")
    text_file1 = parse_text_file("id", "name", "temp/text0")
    ops = text_file0.get_operations(text_file1)
    assert len(ops) == 1
    assert isinstance(ops[0], OP_MDL_Insert)
    assert ops[0].path == [1]
    assert ops[0].value == ["line3"]


def test_get_operations_insert_multiple_middle(setup_text_files):
    text_file0 = parse_text_file("id", "name", "temp/text0")
    create_text_file("temp/text0", "line1\nline3\nline4\nline2")
    text_file1 = parse_text_file("id", "name", "temp/text0")
    ops = text_file0.get_operations(text_file1)
    assert len(ops) == 2
    assert isinstance(ops[0], OP_MDL_Insert)
    assert isinstance(ops[1], OP_MDL_Insert)
    assert ops[0].path == [1]
    assert ops[0].value == ["line3"]
    assert ops[1].path == [2]
    assert ops[1].value == ["line4"]

def test_get_operations_remove(setup_text_files):
    text_file0 = parse_text_file("id", "name", "temp/text0")
    create_text_file("temp/text0", "line1")
    text_file1 = parse_text_file("id", "name", "temp/text0")
    ops = text_file0.get_operations(text_file1)
    assert len(ops) == 1
    assert isinstance(ops[0], OP_MDL_Remove)
    assert ops[0].path == [1]
    assert ops[0].value == ["line2"]

def test_get_operations_remove_all(setup_text_files):
    text_file0 = parse_text_file("id", "name", "temp/text0")
    create_text_file("temp/text0", "")
    text_file1 = parse_text_file("id", "name", "temp/text0")
    ops = text_file0.get_operations(text_file1)

    assert len(ops) == 2
    assert isinstance(ops[0], OP_MDL_Remove)
    assert ops[0].path == []
    assert ops[0].value == ["line1", "line2"]
    assert isinstance(ops[1], OP_MDL_Insert)
    assert ops[1].path == []
    assert ops[1].value == []

def test_get_operations_remove_mulitple(setup_text_files):
    create_text_file("temp/text0", "1\n2\n3\n4")
    text_file0 = parse_text_file("id", "name", "temp/text0")
    create_text_file("temp/text0", "1\n4\n")
    text_file1 = parse_text_file("id", "name", "temp/text0")
    ops = text_file0.get_operations(text_file1)
    assert len(ops) == 2
    assert isinstance(ops[0], OP_MDL_Remove)
    assert ops[0].path == [2]
    assert ops[0].value == ["3"]
    assert isinstance(ops[1], OP_MDL_Remove)
    assert ops[1].path == [1]
    assert ops[1].value == ["2"]

def test_get_operations_insert_remove_change(setup_text_files):
    create_text_file("temp/text0", "line1\nline2111\nline3\nline4")
    text_file0 = parse_text_file("id", "name", "temp/text0")
    create_text_file("temp/text0", "line1\nline211\nline4\nxyz")
    text_file1 = parse_text_file("id", "name", "temp/text0")

    ops = text_file0.get_operations(text_file1)
    print(ops)
    assert len(ops) == 3
    assert isinstance(ops[0], OP_MDL_Remove)
    assert isinstance(ops[1], OP_MDL_Insert)
    assert isinstance(ops[2], OP_MDL_Change)

    assert ops[0].path == [2]
    assert ops[0].value == ["line3"]
    assert ops[1].path == [3]
    assert ops[1].value == ["xyz"]
    assert ops[2].path == [1]
    assert ops[2].old_value == ["line2111"]
    assert ops[2].new_value == ["line211"]


def test_complex_operations(setup_text_files):
    old_code_list = [
        "for (int i = 0; i < 100; i++ ) {",
        "System.out.println(i * 2);",
        "int temp = i * 1000;",
        "if (temp < i) {",
        "System.out.println(temp, i);",
        "}",
        "}",
    ]
    old_code = "\n".join(old_code_list)
    new_code_list = [
        "for (int j = 0; j < 100; j++ ) {",
        "int temp1 = j * 1000;",
        "if (temp1 < j) {",
        "System.out.println(temp1, j);",
        "}",
        "}",
    ]
    new_code = "\n".join(new_code_list)

    create_text_file("temp/text0", old_code)
    text_file0 = parse_text_file("id", "name", "temp/text0")
    create_text_file("temp/text0", new_code)
    text_file1 = parse_text_file("id", "name", "temp/text0")

    ops = text_file0.get_operations(text_file1)
    print(ops)
    assert len(ops) == 5
    assert isinstance(ops[0], OP_MDL_Remove)
    assert isinstance(ops[1], OP_MDL_Change)
    assert isinstance(ops[2], OP_MDL_Change)
    assert isinstance(ops[3], OP_MDL_Change)
    assert isinstance(ops[4], OP_MDL_Change)

    assert ops[0].path == [1]
    assert ops[0].value == [old_code_list[1]]
    assert ops[1].path == [0]
    assert ops[1].old_value == [old_code_list[0]]
    assert ops[1].new_value == [new_code_list[0]]
    assert ops[2].path == [1]
    assert ops[2].old_value == [old_code_list[2]]
    assert ops[2].new_value == [new_code_list[1]]
    assert ops[3].path == [2]
    assert ops[3].old_value == [old_code_list[3]]
    assert ops[3].new_value == [new_code_list[2]]
    assert ops[4].path == [3]
    assert ops[4].old_value == [old_code_list[4]]
    assert ops[4].new_value == [new_code_list[3]]





