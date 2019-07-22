import copy
from version_control.State import State
from version_control.Operation import Operation

class JSONOpListInsert(Operation):

    def __init__(self, file_name, path, new_value):
        self.file_name = file_name
        self.path = path
        self.new_value = new_value

    def apply_operation(self, state):
        if not self.valid_operation(state):
            return None

        files = copy.deepcopy(state.files)
        self.apply_operation_to_file(files[self.file_name])
        
        return State(files)

    def apply_operation_to_file(self, file):
        file.insert(self.path, self.new_value)

    def valid_operation(self, state):
        try:
            curr_obj = state.files[self.file_name].file_contents
            for step in self.path[:-1]:
                curr_obj = curr_obj[step]
            line_number = int(self.path[-1])
            return line_number >= 0 and len(curr_obj) >= line_number
        except:
            return False
        return True

    def to_string(self):
        pass

    @staticmethod
    def from_string(operation_string):
        pass