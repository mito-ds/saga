import pickle
import hashlib
from copy import deepcopy
from saga.operation_utils import parse_operation

class Patch():

    def __init__(self, operations):
        self.operations = operations # set of operation objects

    def apply_patch(self, state):
        curr_state = deepcopy(state)
        curr_state.prev_state_hash = state.get_hash()
        for operation in self.operations:
            curr_state = operation.apply_operation(curr_state)
            if curr_state is None:
                return None

        return curr_state

    def insert_operation(self, operation):
        self.operations.insert(operation)

    def get_hash(self):
        m = hashlib.sha256()
        m.update(bytearray(self.to_string()))
        return m.hexdigest()

    def to_string(self):
        return pickle.dumps(self)

    @staticmethod
    def from_string(patch_str):
        return pickle.loads(patch_str)
