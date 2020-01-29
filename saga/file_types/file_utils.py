from pathlib import Path
from saga.file_types.binary_file import parse_binary_file, write_binary_file
from saga.file_types.text_file import parse_text_file, write_text_file
from saga.file_types.csv_file import parse_csv_file, write_csv_file
from saga.file_types.excel_file import parse_excel_file, write_excel_file


def is_csv(file_path: Path):
    return file_path.suffix == ".csv"


TEXT_ENDINGS = {
    ".txt",  # just text
    ".py",  # python
    ".c",  # c source
    ".cc",  # c++ source
    ".java",  # java source
    ".js",  # js source
    ".php"  # php source
}


def is_text(file_path: Path):
    return file_path.suffix in TEXT_ENDINGS


def is_excel(file_path: Path):
    return file_path.suffix == ".xlsx"


def parse_file(file_id, file_name, file_path):
    if is_text(file_path):
        return parse_text_file(file_id, file_name, file_path)
    elif is_excel(file_path):
        return parse_excel_file(file_id, file_name, file_path)
    elif is_csv(file_path):
        return parse_csv_file(file_id, file_name, file_path)
    else:
        return parse_binary_file(file_id, file_name, file_path)


def write_file(file):
    if file.file_type == "csv":
        write_csv_file(file)
    elif file.file_type == "text":
        write_text_file(file)
    elif file.file_type == "binary":
        write_binary_file(file)
    elif file.file_type == "excel":
        write_excel_file(file)
    else:
        print("Error: file type {} does not exist".format(file.file_type))
