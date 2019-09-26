from saga.base_file.File import File
from saga.data_types.multi_dim_list.MultiDimList import MultiDimList
import csv

def parse_csv_file(file_id, file_name, file_path):
    file_contents = []
    with open(file_path) as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            file_contents.append(row)

    l = MultiDimList(file_contents, 2)
    return File(file_id, "csv", file_name, l)

def write_csv_file(file):
    lines = [",".join(row) for row in file.file_contents.multi_dim_list]
    f = open(file.file_name, "w+")
    f.write("\n".join(lines))
    f.close()

