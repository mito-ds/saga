import pytest
import os
from saga.base_file.File import File
from saga.file_types.text_file import parse_text_file, write_text_file

def create_text_file(path, contents):
    if os.path.isfile(path):
        os.remove(path)
    print("path")
    f = open(path, 'w+')
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
    for key in ops:
        assert len(ops[key]) == 0
    
def test_get_operations_insert_end(setup_text_files):
    text_file0 = parse_text_file("id", "name", "temp/text0")
    create_text_file("temp/text0", "line1\nline2\nline3")
    text_file1 = parse_text_file("id", "name", "temp/text0")
    ops = text_file0.get_operations(text_file1)
    assert len(ops["file"]) == 0
    assert len(ops["inserted"]) == 1
    assert ops["inserted"] == [[2]]
    assert len(ops["changed"]) == 0
    assert len(ops["removed"]) == 0

def test_get_operations_insert_middle(setup_text_files):
    text_file0 = parse_text_file("id", "name", "temp/text0")
    create_text_file("temp/text0", "line1\nline3\nline2")
    text_file1 = parse_text_file("id", "name", "temp/text0")
    ops = text_file0.get_operations(text_file1)
    assert len(ops["file"]) == 0
    assert len(ops["inserted"]) == 1
    assert ops["inserted"] == [[1]]
    assert len(ops["changed"]) == 0
    assert len(ops["removed"]) == 0


def test_get_operations_insert_multiple_middle(setup_text_files):
    text_file0 = parse_text_file("id", "name", "temp/text0")
    create_text_file("temp/text0", "line1\nline3\nline4\nline2")
    text_file1 = parse_text_file("id", "name", "temp/text0")
    ops = text_file0.get_operations(text_file1)
    assert len(ops["file"]) == 0
    assert len(ops["inserted"]) == 2
    assert ops["inserted"] == [[1], [2]]
    assert len(ops["changed"]) == 0
    assert len(ops["removed"]) == 0

def test_get_operations_remove(setup_text_files):
    text_file0 = parse_text_file("id", "name", "temp/text0")
    create_text_file("temp/text0", "line1")
    text_file1 = parse_text_file("id", "name", "temp/text0")
    ops = text_file0.get_operations(text_file1)
    assert len(ops["file"]) == 0
    assert len(ops["inserted"]) == 0
    assert len(ops["changed"]) == 0
    assert len(ops["removed"]) == 1
    assert ops["removed"] == [[1]]

def test_get_operations_remove_all(setup_text_files):
    text_file0 = parse_text_file("id", "name", "temp/text0")
    create_text_file("temp/text0", "")
    text_file1 = parse_text_file("id", "name", "temp/text0")
    ops = text_file0.get_operations(text_file1)

    assert len(ops["file"]) == 0
    assert len(ops["inserted"]) == 0
    assert len(ops["changed"]) == 0
    assert len(ops["removed"]) == 2
    assert ops["removed"] == [[0], [1]]

def test_get_operations_remove_mulitple(setup_text_files):
    create_text_file("temp/text0", "1\n2\n3\n4")
    text_file0 = parse_text_file("id", "name", "temp/text0")
    create_text_file("temp/text0", "1\n4\n")
    text_file1 = parse_text_file("id", "name", "temp/text0")
    ops = text_file0.get_operations(text_file1)
    assert len(ops["file"]) == 0
    assert len(ops["inserted"]) == 0
    assert len(ops["changed"]) == 0
    assert len(ops["removed"]) == 2
    assert ops["removed"] == [[1], [2]]

def test_get_operations_insert_remove_change(setup_text_files):
    create_text_file("temp/text0", "line1\nline2111\nline3\nline4")
    text_file0 = parse_text_file("id", "name", "temp/text0")
    create_text_file("temp/text0", "line1\nline211\nline4\nxyz")
    text_file1 = parse_text_file("id", "name", "temp/text0")

    ops = text_file0.get_operations(text_file1)
    
    assert len(ops["file"]) == 0
    assert len(ops["inserted"]) == 1
    assert ops["inserted"] == [[3]]
    assert len(ops["changed"]) == 1
    assert ops["changed"] == [[1]]
    assert len(ops["removed"]) == 1
    assert ops["removed"] == [[2]]

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

    assert len(ops["file"]) == 0
    assert len(ops["inserted"]) == 0
    assert len(ops["changed"]) == 4
    assert ops["changed"] == [[0], [2], [3], [4]]
    assert len(ops["removed"]) == 1
    assert ops["removed"] == [[1]]


def test_merge():
    from tests.test_utils import do_test_merge
    for path in os.listdir("tests/merges/text"):
        path = os.path.join("tests/merges/text", path)
        if os.path.isdir(path):
            assert do_test_merge(path, ".txt")