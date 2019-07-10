import copy

class State():

    def __init__(self, files):
        # map from file id -> contents
        self.files = files 

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


class Patch():

    def __init__(self, operations):
        self.operations = operations # set of operation objects

    def apply_patch(self, state):
        curr_state = state
        for operation in self.operations:
            curr_state = operation.apply_operation(curr_state)
            if curr_state is None:
                return None

        return curr_state

class Branch():

    def __init__(self):
        self.patches = []
        self.states = [State(dict())] # state 0 is the empty state

    def add_patch(self, patch):
        # try and apply the new patch
        old_state = self.states[-1]
        new_state = patch.apply_patch(old_state)
        if new_state is None:
            raise Exception("Invalid patch to add to branch")
        self.states.append(new_state)
        self.patches.append(patch)
