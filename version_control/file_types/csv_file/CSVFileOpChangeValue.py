import copy
from version_control.State import State
from version_control.Operation import Operation

class CSVFileOpChangeValue(Operation):

    def __init__(self, file_name, row, column, value):
        self.file_name = file_name
        self.row = row
        self.column = column
        self.value = value

    def apply_operation(self, state):
        if not self.valid_operation(state):
            return None

        files = copy.deepcopy(state.files)
        self.apply_operation_to_file(files[self.file_name])
        
        return State(files)

    def apply_operation_to_file(self, file):
        file.change_value(self.row, self.column, self.value)

    def valid_operation(self, state):
        if self.file_name not in state.files:
            return False
        return True

    def to_string(self):
        return "CSVFileChangeValue\t{}\t{}\t{}\t{}".format(self.file_name, self.row, self.column, self.value)

    @staticmethod
    def from_string(operation_string):
        operation = operation_string.split("\t")
        return CSVFileOpChangeValue(operation[1], operation[2], operation[3], operation[4])