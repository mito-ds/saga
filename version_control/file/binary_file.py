from version_control.file.File import File
from version_control.data_types.multi_dim_list.MultiDimList import MultiDimList

def parse_binary_file(file_path):
    f = open(file_path, "r")
    file_contents = [f.read()]
    f.close()
    l = MultiDimList(file_contents, 1)
    return File(file_path, "binary", file_path, l)

def write_binary_file(self, file):
    f = open(self.file_name, "wb+")
    f.write(bytes(self.file_contents.mutli_dim_list[0], "utf-8"))
    f.close()

