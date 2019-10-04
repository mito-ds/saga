from saga.base_file.File import File
import csv

def parse_csv_file(file_id, file_name, file_path):
    file_contents = []
    with open(file_path) as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            file_contents.append(row)

    return File(file_id, "csv", file_path, file_name, file_contents)

def write_csv_file(file):
    lines = [",".join(row) for row in file.file_contents.mixed_data_type]
    f = open(file.file_path, "w+")
    f.write("\n".join(lines))
    f.close()

