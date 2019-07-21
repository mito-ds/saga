from copy import deepcopy
from psd_tools import PSDImage
from version_control.file_types.file.File import File


class PhotoshopFile(File):

    def __init__(self, file_name):
        File.__init__(self, file_name)
        psd = PSDImage.open(file_name)
        print(psd.__dict__)

        for layer in psd:
            print(layer)
