from copy import deepcopy
from saga.Operation import Operation

class OP_File_ChangeName(Operation):

    def __init__(self, file_id, old_name, new_name):
        Operation.__init__(self, "OP_File_ChangeName", file_id)
        self.old_name = old_name
        self.new_name = new_name

    def apply_operation_to_file(self, file):
        # TODO: figure out how we might extend this notion of invalidity to paths in list:
        # because we might insert a bunch of lines at the start of a file,
        # the old path might point to different values (and it would still be valid)
        if file.file_name != self.old_name:
            raise Exception("Invalid operation")

        file.file_name = self.new_name
        return file

    def inverse(self):
        return OP_File_ChangeName(self.file_id, self.new_name, self.old_name)

    def __str__(self):
        return "OP_File_ChangeName: changed file {} to {}".format(self.old_name, self.new_name)