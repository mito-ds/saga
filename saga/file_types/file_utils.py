import csv
from saga.file_types.binary_file import parse_binary_file, write_binary_file
from saga.file_types.text_file import parse_text_file, write_text_file
from saga.file_types.csv_file import parse_csv_file, write_csv_file
from saga.file_types.excel_file import parse_excel_file, write_excel_file

def is_csv(file_path):
    return file_path.endswith(".csv")

TEXT_ENDINGS = {
    "txt", # just text
    "py", # python
    "c", # c source
    "cc", # c++ source 
    "java", # java source 
    "js",
    "php"
}

def is_text(file_path):
    try:
        ending = file_path.split(".")[-1]
        return ending in TEXT_ENDINGS
    except:
        return False

def is_excel(file_path):
    return file_path.endswith(".xlsx")


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