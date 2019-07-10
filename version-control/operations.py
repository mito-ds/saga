import copy
from State import State

class Operation():

    def __init__(self, name):
        self.name = name

    def apply_operation(self, state):
        """
        Returns the new state if the operation is valid on the state.
        Otherwise returns None
        """
        raise NotImplementedError("Must be implemented by specific operation")

    def valid_operation(self, state):
        """
        Returns True if the operation is valid on the state.
        Otherwise returns False
        """
        raise NotImplementedError("Must be implemented by specific operation")

class AddFileOperation(Operation):

    def __init__(self, new_file, new_file_contents):
        self.new_file = new_file
        self.new_file_contents = new_file_contents

    def apply_operation(self, state):
        if not self.valid_operation(state):
            return None

        files = copy.deepcopy(state.files)
        files[self.new_file] = self.new_file_contents
        
        return State(files)

    def valid_operation(self, state):
        return self.new_file not in state.files