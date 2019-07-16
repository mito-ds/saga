import copy
from version_control.State import State
from version_control.Operation import Operation
from version_control.file_utils import parse_file

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
    
    def to_string(self):
        return "FileOpAdd\t{}\t{}".format(self.file_name, self.file.to_string())

    @staticmethod
    def from_string(operation_string):
        operation = operation_string.split("\t")
        file_string = "\t".join(operation[2:])
        file_obj = parse_file(file_string)
        return FileOpAdd(operation[1], file_obj)