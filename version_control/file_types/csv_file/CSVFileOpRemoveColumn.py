import copy
from version_control.State import State
from version_control.Operation import Operation

class CSVFileOpRemoveColumn(Operation):

    def __init__(self, file_name, index):
        self.file_name = file_name
        self.index = index

    def apply_operation(self, state):
        if not self.valid_operation(state):
            return None

        files = copy.deepcopy(state.files)
        self.apply_operation_to_file(files[self.file_name])
        
        return State(files)

    def apply_operation_to_file(self, file):
        file.remove_column(self.index)

    def valid_operation(self, state):
        if self.file_name not in state.files:
            return False
        return True

    def to_string(self):
        return "CSVFileRemoveColumn\t{}\t{}".format(self.file_name, self.index)

    @staticmethod
    def from_string(operation_string):
        operation = operation_string.split("\t")
        return CSVFileOpRemoveColumn(operation[1], operation[2])