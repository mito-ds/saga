import copy
from version_control.State import State
from version_control.Operation import Operation

class JSONOpInsert(Operation):

    def __init__(self, file_name, path, value, move_list=False):
        self.file_name = file_name
        self.path = path
        self.value = value
        # move list is true when you want to add a new element to a list
        # as compared to changing an element in a list to a new element
        self.move_list = move_list

    def apply_operation(self, state):
        if not self.valid_operation(state):
            return None

        files = copy.deepcopy(state.files)
        self.apply_operation_to_file(files[self.file_name])
        
        return State(files)

    def apply_operation_to_file(self, file):
        file.insert(self.path, self.value, self.move_list)

    def valid_operation(self, state):
        if self.file_name not in state.files:
            return False
        return True # TODO: check if path is in jawn

    def to_string(self):
        pass

    @staticmethod
    def from_string(operation_string):
        pass