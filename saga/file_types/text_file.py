from saga.base_file.File import File


def parse_text_file(file_id, file_name, file_path):
    f = open(file_path, "r")
    file_contents = []
    for line in f.readlines():
        if line.endswith("\n"):
            file_contents.append(line[:len(line) - 1])
        else:
            file_contents.append(line)

    return File(file_id, "text", file_path, file_name, file_contents)


def write_text_file(file):
    f = open(file.file_path, "w+")
    f.write("\n".join(file.file_contents.mixed_data_type))
    f.close()