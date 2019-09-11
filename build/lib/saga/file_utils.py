from version_control.file_types.binary_file.BinaryFile import BinaryFile
from version_control.file_types.text_file.TextFile import TextFile


FILE_DICT = {
    "BinaryFile": BinaryFile,
    "TextFile": TextFile
}

def parse_file(file_string):
    file_s = file_string.split("\t")
    file_class = FILE_DICT[file_s[0]]
    return file_class.from_string(file_string)
