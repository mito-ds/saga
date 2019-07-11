from version_control.file_types.file.File import File
from version_control.file_types.binary_file.BinaryOpChangeContents import BinaryOpChangeContents

class BinaryFile(File):

    def __init__(self, file_name, file_contents):
        File.__init__(self, file_name)
        self.file_contents = file_contents

    def get_operations(self, new_file):
        # get the changes between this file and the previous one
        if new_file.file_name != self.file_name:
            raise Exception("Can only get operations on the same files")
        if self.file_contents == new_file.file_contents:
            return []
        return [BinaryOpChangeContents(self.file_name, new_file.file_contents)]

    # there's not much here, tbh
    def change_contents(self, file_contents):
        self.file_contents = file_contents
