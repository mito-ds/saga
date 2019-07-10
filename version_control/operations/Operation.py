from version_control.State import State

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