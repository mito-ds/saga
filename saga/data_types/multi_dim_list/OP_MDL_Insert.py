import copy
from saga.Operation import Operation

class OP_MDL_Insert(Operation):

    def __init__(self, file_id, path, value):
        Operation.__init__(self, "OP_MDL_Insert", file_id)
        self.path = path
        self.value = value

    def apply_operation_to_file(self, file):
        if self.file_id != file.file_id:
            raise ValueError("Wrong file provided")

        file.file_contents.insert_path(self.path, self.value)
        return file

    def inverse(self):
        from saga.data_types.multi_dim_list.OP_MDL_Remove import OP_MDL_Remove 
        return OP_MDL_Remove(self.file_id, self.path, self.value)

    def __str__(self):
        return "OP_MDL_Insert: at path {}, inserted {}".format(self.path, self.value)