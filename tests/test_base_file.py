import pytest
from saga.base_file.File import File
from saga.base_file.OP_File_Insert import OP_File_Insert
from saga.base_file.OP_File_Remove import OP_File_Remove
from saga.base_file.OP_File_ChangeName import OP_File_ChangeName

def blank_insert():
    return OP_File_Insert("id", "type", "name", "contents")

def blank_remove():
    return OP_File_Remove("id", "type", "name", "contents")

# TODO