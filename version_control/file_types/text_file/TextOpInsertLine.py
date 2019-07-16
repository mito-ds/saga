import copy
from version_control.State import State
from version_control.Operation import Operation

class TextOpInsertLine(Operation):

    def __init__(self, file_name, line_number, line_contents):
        self.file_name = file_name
        self.line_number = line_number
        self.line_contents = line_contents

    def apply_operation(self, state):
        if not self.valid_operation(state):
            return None

        files = copy.deepcopy(state.files)
        self.apply_operation_to_file(files[self.file_name])
        
        return State(files)

    def apply_operation_to_file(self, file):
        file.insert_line(self.line_number, self.line_contents)

    def valid_operation(self, state):
        if self.file_name not in state.files:
            return False
        return self.line_number >= 0 and len(state.files[self.file_name].file_contents) >= self.line_number

    def to_string(self):
        return "TextOpInsertLine\t{}\t{}\t{}".format(self.file_name, self.line_number, self.line_contents)

    @staticmethod
    def from_string(operation_string):
        operation = operation_string.split("\t")
        return TextOpInsertLine(operation[1], int(operation[2]), operation[3])