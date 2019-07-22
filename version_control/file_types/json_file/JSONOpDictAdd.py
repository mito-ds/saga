import copy
from version_control.State import State
from version_control.Operation import Operation

class JSONOpDictAdd(Operation):

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
        file.set_path(self.path, self.new_value)

    def valid_operation(self, state):
        try:
            curr_obj = state.files[self.file_name].file_contents
            for step in self.path[:-1]:
                print("STEP: {}".format(step))
                curr_obj = curr_obj[step]
        except:
            return False
        return True

    def to_string(self):
        pass

    @staticmethod
    def from_string(operation_string):
        pass