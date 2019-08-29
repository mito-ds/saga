import pytest
import os
import json
from version_control.Patch import Patch
from version_control.Branch import Branch
from version_control.file_types.csv_file.CSVFile import CSVFile
from version_control.file_types.csv_file.CSVFileOpAddRow import CSVFileOpAddRow
from version_control.file_types.csv_file.CSVFileOpRemoveRow import CSVFileOpRemoveRow
from version_control.file_types.csv_file.CSVFileOpAddColumn import CSVFileOpAddColumn
from version_control.file_types.csv_file.CSVFileOpRemoveColumn import CSVFileOpRemoveColumn
from version_control.file_types.csv_file.CSVFileOpChangeValue import CSVFileOpChangeValue


def test_delete_row():
    csv_old = CSVFile("filename", [["a", "b"], ["c", "d"]])
    csv_new = CSVFile("filename", [["a", "b"]])

    assert csv_old.get_operations(csv_new)[0].index == 1
    assert isinstance(csv_old.get_operations(csv_new)[0], CSVFileOpRemoveRow)


def test_add_row():
    csv_old = CSVFile("filename", [["a", "b"]])
    csv_new = CSVFile("filename", [["a", "b"], ["c", "d"]])

    assert csv_old.get_operations(csv_new)[0].index == 1
    assert csv_old.get_operations(csv_new)[0].value[0] == "c"
    assert csv_old.get_operations(csv_new)[0].value[1] == "d"
    assert isinstance(csv_old.get_operations(csv_new)[0], CSVFileOpAddRow)



def test_add_and_deleterow():
    csv_old = CSVFile("filename", [["a", "b"], ["c", "d"]])
    csv_new = CSVFile("filename", [["a", "b"], ["e", "f"]])

    assert csv_old.get_operations(csv_new)[0].index == 1
    assert isinstance(csv_old.get_operations(csv_new)[0], CSVFileOpRemoveRow)
    assert csv_old.get_operations(csv_new)[1].value[0] == "e"
    assert csv_old.get_operations(csv_new)[1].value[1] == "f"
    assert isinstance(csv_old.get_operations(csv_new)[1], CSVFileOpAddRow)


def test_delete_column():
    csv_old = CSVFile("filename", [["a", "b"], ["c", "d"]])
    csv_new = CSVFile("filename", [["a"], ["c"]])

    assert csv_old.get_operations(csv_new)[0].index == 1
    assert isinstance(csv_old.get_operations(csv_new)[0], CSVFileOpRemoveColumn)

def test_add_column():
    csv_old = CSVFile("filename", [["a"], ["c"]])
    csv_new = CSVFile("filename", [["a", "b"], ["c", "d"]])

    assert csv_old.get_operations(csv_new)[0].index == 1
    assert csv_old.get_operations(csv_new)[0].value[0] == "b"
    assert csv_old.get_operations(csv_new)[0].value[1] == "d"
    assert isinstance(csv_old.get_operations(csv_new)[0], CSVFileOpAddColumn)


def test_delete_column_and_row():
    csv_old = CSVFile("filename", [["a", "b", "c"], ["d", "e", "f"], ["g", "h", "i"]])
    csv_new = CSVFile("filename", [["a", "b"], ["d", "e"]])

    assert csv_old.get_operations(csv_new)[0].index == 2
    assert isinstance(csv_old.get_operations(csv_new)[0], CSVFileOpRemoveRow)

    assert csv_old.get_operations(csv_new)[1].index == 2
    assert isinstance(csv_old.get_operations(csv_new)[1], CSVFileOpRemoveColumn)


def test_delete_row_insert_col_delete_row_insert_col():
    csv_old = CSVFile("filename", [["a", "b", "c"], ["d", "e", "f"], ["g", "h", "i"]])
    csv_new = CSVFile("filename", [["a", "b"], ["d", "e"], ["z", "y"]])

    assert csv_old.get_operations(csv_new)[0].index == 2
    assert isinstance(csv_old.get_operations(csv_new)[0], CSVFileOpRemoveRow)

    assert csv_old.get_operations(csv_new)[1].index == 2
    assert csv_old.get_operations(csv_new)[1].value[0] == "z"
    assert csv_old.get_operations(csv_new)[1].value[1] == "y"
    assert isinstance(csv_old.get_operations(csv_new)[1], CSVFileOpAddRow)

    op = csv_old.get_operations(csv_new)[2].index
    assert csv_old.get_operations(csv_new)[2].index == 2
    assert isinstance(csv_old.get_operations(csv_new)[2], CSVFileOpRemoveColumn)


def test_change_value_partial():
    csv_old = CSVFile("filename", [["a", "b"], ["c", "de"]])
    csv_new = CSVFile("filename", [["a", "b"], ["c", "e"]])

    op = csv_old.get_operations(csv_new)

    assert len(csv_old.get_operations(csv_new)) == 1
    assert csv_old.get_operations(csv_new)[0].row == 1
    assert csv_old.get_operations(csv_new)[0].column == 1
    assert isinstance(csv_old.get_operations(csv_new)[0], CSVFileOpChangeValue)

def test_change_value_full():
    csv_old = CSVFile("filename", [["a", "b"], ["c", "d"]])
    csv_new = CSVFile("filename", [["a", "b"], ["c", "e"]])

    op = csv_old.get_operations(csv_new)

    assert len(csv_old.get_operations(csv_new)) == 1
    assert csv_old.get_operations(csv_new)[0].row == 1
    assert csv_old.get_operations(csv_new)[0].column == 1
    assert isinstance(csv_old.get_operations(csv_new)[0], CSVFileOpChangeValue)
