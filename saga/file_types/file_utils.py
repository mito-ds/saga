import csv
from saga.file_types.binary_file import parse_binary_file, write_binary_file
from saga.file_types.text_file import parse_text_file, write_text_file
from saga.file_types.csv_file import parse_csv_file, write_csv_file

def is_csv(file_path):
    csv_fileh = open(file_path, 'r')
    try:
        _ = csv.Sniffer().sniff(csv_fileh.read(1024))
        csv_fileh.seek(0)
        return True
    except csv.Error:
        return False


def parse_file(file_id, file_name, file_path):
    if file_path.endswith(".txt"):
        return parse_text_file(file_id, file_name, file_path)
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
    else:
        print("Error: file type {} does not exist".format(file.file_type))