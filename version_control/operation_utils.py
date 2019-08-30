from version_control.file_types.file.FileOpAdd import FileOpAdd
from version_control.file_types.file.FileOpRemove import FileOpRemove
from version_control.file_types.binary_file.BinaryOpChangeContents import BinaryOpChangeContents
from version_control.file_types.text_file.TextOpInsertLine import TextOpInsertLine
from version_control.file_types.text_file.TextOpRemoveLine import TextOpRemoveLine

OPERATION_DICT = {
    "FileOpAdd": FileOpAdd,
    "FileOpRemove": FileOpRemove,
    "BinaryOpChangeContents": BinaryOpChangeContents,
    "TextOpInsertLine": TextOpInsertLine,
    "TextOpRemoveLine": TextOpRemoveLine
}

def parse_operation(operation_string):
    operation = operation_string.split("\t")
    operation_class = OPERATION_DICT[operation[0]]
    return operation_class.from_string(operation_string)
