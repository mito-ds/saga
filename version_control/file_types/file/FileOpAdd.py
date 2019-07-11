import copy
from version_control.State import State
from version_control.Operation import Operation

class FileOpAdd(Operation):

    def __init__(self, file_name, file):
        # TODO: maybe should take in File type, and create a new empty file of that sort? 
        self.file_name = file_name
        self.file = file

    def apply_operation(self, state):
        if not self.valid_operation(state):
            return None

        files = copy.deepcopy(state.files)
        files[self.file_name] = self.file
        
        return State(files)

    def valid_operation(self, state):
        return self.file_name not in state.files