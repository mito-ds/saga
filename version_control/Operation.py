
class Operation():

    def __init__(self, name):
        self.name = name

    def apply_operation(self, state):
        """
        Returns the new state if the operation is valid on the state.
        Otherwise returns None
        """
        raise NotImplementedError("Must be implemented by specific operation")

    def apply_operation_to_file(self, file):
        """
        Returns a modified version of the file, with the ooeration applied
        """
        raise NotImplementedError("Must be implemented by specific operation")


    def valid_operation(self, state):
        """
        Returns True if the operation is valid on the state.
        Otherwise returns False
        """
        raise NotImplementedError("Must be implemented by specific operation")

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
