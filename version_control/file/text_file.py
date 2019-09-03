from version_control.file.File import File
from version_control.data_types.multi_dim_list.MultiDimList import MultiDimList


def parse_text_file(self, file_path):
    f = open(file_path, "r")
    file_contents = []
    for line in f.readlines():
        if line.endswith("\n"):
            file_contents.append(line[:len(line) - 1])
        else:
            file_contents.append(line)
    l = MultiDimList(file_contents, 1)

    return File(file_path, "text", file_path, l)


def write_text_file(self, file):
    f = open(file.file_name, "w+")
    f.write("\n".join(file.file_contents.multi_dim_list))
    f.close()