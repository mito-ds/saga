
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

    def add_operation(self, operation):
        self.operations.add(operation)