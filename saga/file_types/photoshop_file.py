from saga.base_file.File import File
from psd_tools import PSDImage


def parse_photoshop_file(file_id, file_name, file_path):
    # TODO
    psd = PSDImage.open(file_path)
    data = [layer._record for layer in psd]
    for x in data:
        print(x)
    return File(file_id, "photoshop", file_path, file_name, data)


def write_photoshop_file(file):
    # TODO
    print("here also")


