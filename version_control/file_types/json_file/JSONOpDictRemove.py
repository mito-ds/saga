import copy
from version_control.State import State
from version_control.Operation import Operation

class JSONOpDictRemove(Operation):

    def __init__(self, file_name, path):
        self.file_name = file_name
        self.path = path

    def apply_operation(self, state):
        if not self.valid_operation(state):
            return None

        files = copy.deepcopy(state.files)
        self.apply_operation_to_file(files[self.file_name])
        
        return State(files)

    def apply_operation_to_file(self, file):
        file.remove(self.path)

    def valid_operation(self, state):
        if self.file_name not in state.files:
            return False
        return True # TODO: check if path is in jawn

    def to_string(self):
        pass

    @staticmethod
    def from_string(operation_string):
        pass