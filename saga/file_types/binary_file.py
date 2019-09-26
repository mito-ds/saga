from saga.base_file.File import File
from saga.data_types.multi_dim_list.MultiDimList import MultiDimList

def parse_binary_file(file_id, file_name, file_path):
    f = open(file_path, "r")
    file_contents = [f.read()]
    f.close()
    l = MultiDimList(file_contents, 1)
    return File(file_id, "binary", file_name, l)

def write_binary_file(file):
    f = open(file.file_name, "wb+")
    f.write(bytes(file.file_contents.multi_dim_list[0], "utf-8"))
    f.close()

