import pytest
import os
from saga.base_file.File import File
from saga.file_types.csv_file import parse_csv_file, write_csv_file

def create_csv_file(name, contents):
    if os.path.isfile(name):
        os.remove(name)
    f = open(name, 'w+')
    f.write(contents)
    f.close()

@pytest.fixture()
def setup_csv_files():
    if not os.path.isdir("temp"):
        os.mkdir('temp')
    create_csv_file("temp/csv0", "name,email\ntest,test@gmail.com")

def test_create(setup_csv_files):
    csv_file = parse_csv_file("id", "name", "temp/csv0")
    assert csv_file.file_name == "name"
    assert csv_file.file_contents.mixed_data_type == [["name", "email"], ["test", "test@gmail.com"]]

def test_create_then_write(setup_csv_files):
    csv_file = parse_csv_file("id", "name", "temp/csv0")
    write_csv_file(csv_file)
    f = open('temp/csv0', 'r')
    assert f.read() == "name,email\ntest,test@gmail.com"

def test_get_operations_no_change(setup_csv_files):
    csv_file0 = parse_csv_file("id", "name", "temp/csv0")
    csv_file1 = parse_csv_file("id", "name", "temp/csv0")
    ops = csv_file0.get_operations(csv_file1)
    for key in ops:
        assert len(ops[key]) == 0
    
def test_get_operations_insert_row(setup_csv_files):
    csv_file0 = parse_csv_file("id", "name", "temp/csv0")
    create_csv_file("temp/csv0", "name,email\ntest,test@gmail.com\nharry,harry@gmail.com")
    csv_file1 = parse_csv_file("id", "name", "temp/csv0")
    ops = csv_file0.get_operations(csv_file1)
    assert len(ops["file"]) == 0
    assert len(ops["changed"]) == 0
    assert len(ops["inserted"]) == 1
    assert ops["inserted"] == [[2]]
    assert len(ops["removed"]) == 0
