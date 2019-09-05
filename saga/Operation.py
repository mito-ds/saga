from copy import deepcopy

class Operation():

    def __init__(self, op_name, file_id):
        self.op_name = op_name
        self.file_id = file_id

    def apply_operation(self, state):
        try:
            file = state[self.file_id]
            state[self.file_id] = self.apply_operation_to_file(file)
            return deepcopy(state)
        except:
            return None

    def apply_operation_to_file(self, file):
        """
        Returns a modified version of the file, with the ooeration applied
        """
        raise NotImplementedError("Must be implemented by specific operation")


    def inverse(self):
        """
        Returns an operation that when applied after this operation will result in the
        initial state
        """
        raise NotImplementedError("Must be implemented by specific operation")

    # TODO: come up some some way of storing these data blobs, maybe lik git does. 

    def to_string(self):
        """
        Returns the operation written to a string
        """
        raise NotImplementedError("Must be implemented by specific operation")


    @staticmethod
    def from_string(operation_string):
        """
        Returns an instance of the operation parsed from a valid operation string
        """
        raise NotImplementedError("Must be implemented by specific operation")
