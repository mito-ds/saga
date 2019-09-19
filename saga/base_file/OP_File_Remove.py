from copy import deepcopy
from saga.Operation import Operation

class OP_File_Remove(Operation):

    def __init__(self, file_id, file_type, file_name, file_contents):
        Operation.__init__(self, "OP_File_Remove", file_id)
        self.file_type = file_type
        self.file_name = file_name
        self.file_contents = file_contents

    def apply_operation_to_file(self, file):
        if file is None:
            raise Exception("Invalid operation")
        return None

    def inverse(self):
        from saga.base_file.OP_File_Insert import OP_File_Insert
        return OP_File_Insert(self.file_id, self.file_type, self.file_name, self.file_contents)

    def __str__(self):
        return "OP_File_Remove: removed file {} of type {}".format(self.file_name, self.file_type)