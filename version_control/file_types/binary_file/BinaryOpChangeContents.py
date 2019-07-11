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
        files[self.file_name] = self.file_contents
        
        return State(files)

    def valid_operation(self, state):
        return self.file_name in state.files