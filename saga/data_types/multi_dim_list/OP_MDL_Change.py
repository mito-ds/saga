from saga.Operation import Operation

class OP_MDL_Change(Operation):

    def __init__(self, file_id, path, old_value, new_value):
        Operation.__init__(self, "OP_MDL_Change", file_id)
        self.path = path
        self.old_value = old_value
        self.new_value = new_value

    def apply_operation_to_file(self, file):
        if self.file_id != file.file_id:
            raise ValueError("Wrong file provided")

        file.file_contents.change_value(self.path, self.new_value)
        return file

    def inverse(self):
        return OP_MDL_Change(self.file_id, self.path, self.new_value, self.old_value)

    def __str__(self):
        return "OP_MDL_Change: at path {}, changed {} to {}".format(self.path, self.old_value, self.new_value)

    