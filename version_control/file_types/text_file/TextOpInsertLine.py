import copy
from version_control.State import State
from version_control.Operation import Operation

class TextOpAppendLine(Operation):

    def __init__(self, file_name, line_number, line_contents):
        self.file_name = file_name
        self.line_number = line_number
        self.line_contents = line_contents

    def apply_operation(self, state):
        if not self.valid_operation(state):
            return None

        files = copy.deepcopy(state.files)
        files[self.file_name].change_line(self.line_number, self.line_contents)
        
        return State(files)

    def valid_operation(self, state):
        if self.file_name not in state.files:
            return False
        return self.line_number >= 0 and len(state.files[self.file_name].file_contents) > self.line_number