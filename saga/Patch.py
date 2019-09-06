from saga.operation_utils import parse_operation

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

    def insert_operation(self, operation):
        self.operations.insert(operation)

    def to_string(self):
        operation_strings = []
        for operation in self.operations:
            operation_strings.append(operation.to_string())
        return "\n".join(operation_strings)

    @staticmethod
    def from_string(patch_string):
        operation_strings = patch_string.split("\n")
        operations = []
        for operation_string in operation_strings:
            operation = parse_operation(operation_string)
            operations.append(operation)
        return Patch(operations)
