from copy import deepcopy
from saga.Operation import Operation
from saga.base_file.File import File

class OP_File_Insert(Operation):

    def __init__(self, file_id, file_type, file_name, file_contents):
        Operation.__init__(self, "OP_File_Insert", file_id)
        self.file_type = file_type
        self.file_name = file_name
        self.file_contents = file_contents

    def apply_operation_to_file(self, file):
        if file is not None:
            raise Exception("Invalid operation")

        return File(self.file_id, self.file_type, self.file_name, self.file_contents)

    def inverse(self):
        from saga.base_file.OP_File_Remove import OP_File_Remove
        return OP_File_Remove(self.file_id, self.file_type, self.file_name, self.file_contents)

    def __str__(self):
        return "OP_File_Insert: inserted file {} of type {}".format(self.file_name, self.file_type)