from saga.base_file.File import File

def parse_binary_file(file_id, file_name, file_path):
    f = open(file_path, "r")
    file_contents = [f.read()]
    f.close()
    return File(file_id, "binary", file_path, file_name, file_contents)

def write_binary_file(file):
    f = open(file.file_path, "wb+")
    f.write(bytes(file.file_contents.mixed_data_type[0], "utf-8"))
    f.close()

