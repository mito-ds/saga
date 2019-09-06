import pytest
import os
from saga.base_file.File import File
from saga.file_types.csv_file import parse_csv_file, write_csv_file
from saga.data_types.multi_dim_list.OP_MDL_Change import OP_MDL_Change
from saga.data_types.multi_dim_list.OP_MDL_Insert import OP_MDL_Insert
from saga.data_types.multi_dim_list.OP_MDL_Remove import OP_MDL_Remove

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
    csv_file = parse_csv_file("temp/csv0")
    assert csv_file.file_name == "temp/csv0"
    assert csv_file.file_contents.multi_dim_list == [["name", "email"], ["test", "test@gmail.com"]]

def test_create_then_write(setup_csv_files):
    csv_file = parse_csv_file("temp/csv0")
    write_csv_file(csv_file)
    f = open('temp/csv0', 'r')
    assert f.read() == "name,email\ntest,test@gmail.com"

def test_get_operations_no_change(setup_csv_files):
    csv_file0 = parse_csv_file("temp/csv0")
    csv_file1 = parse_csv_file("temp/csv0")
    ops = csv_file0.get_operations(csv_file1)
    assert len(ops) == 0
    
def test_get_operations_insert_row(setup_csv_files):
    csv_file0 = parse_csv_file("temp/csv0")
    create_csv_file("temp/csv0", "name,email\ntest,test@gmail.com\nharry,harry@gmail.com")
    csv_file1 = parse_csv_file("temp/csv0")
    ops = csv_file0.get_operations(csv_file1)
    assert len(ops) == 1
    assert isinstance(ops[0], OP_MDL_Insert)
    assert ops[0].path == [2]
    assert ops[0].value == [["harry", "harry@gmail.com"]]

def test_get_operations_insert_column(setup_csv_files):
    csv_file0 = parse_csv_file("temp/csv0")
    create_csv_file("temp/csv0", "name,email,height\ntest,test@gmail.com,6")
    csv_file1 = parse_csv_file("temp/csv0")
    ops = csv_file0.get_operations(csv_file1)
    assert len(ops) == 1
    assert isinstance(ops[0], OP_MDL_Insert)
    assert ops[0].path == ["_", 2]
    assert ops[0].value == ["height", "6"]

def test_get_operations_insert_rows_and_column(setup_csv_files):
    csv_file0 = parse_csv_file("temp/csv0")
    create_csv_file("temp/csv0", "name,email,height\ntest,test@gmail.com,6\nharry,harry@gmail.com,7")
    csv_file1 = parse_csv_file("temp/csv0")
    ops = csv_file0.get_operations(csv_file1)
    assert len(ops) == 2
    assert isinstance(ops[0], OP_MDL_Insert)
    assert isinstance(ops[1], OP_MDL_Insert)
    assert ops[0].path == [2]
    assert ops[0].value == [["harry", "harry@gmail.com", "7"]]

    assert ops[1].path == ["_", 2]
    assert ops[1].value == ["height", "6", "7"]

