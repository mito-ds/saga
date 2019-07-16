import copy
from version_control.State import State
from version_control.Operation import Operation

class BinaryOpChangeContents(Operation):

    def __init__(self, file_name, file_contents):
        self.file_name = file_name
        self.file_contents = file_contents

    def apply_operation(self, state):
        if not self.valid_operation(state):
            return None

        files = copy.deepcopy(state.files)
        files[self.file_name].file_contents = self.file_contents
        
        return State(files)

    def valid_operation(self, state):
        return self.file_name in state.files

    def to_string(self):
        return "BinaryOpChangeContents\t{}\t{}".format(self.file_name, self.file_contents)

    @staticmethod
    def from_string(operation_string):
        operation = operation_string.split("\t")
        return BinaryOpChangeContents(operation[1], operation[2])