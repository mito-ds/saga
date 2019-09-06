from saga.State import State

class Branch():

    def __init__(self):
        self.patches = []
        # Set the initial state to be the empty state
        self.states = [State(dict())]

    def insert_patch(self, patch):
        old_state = self.states[-1]
        new_state = patch.apply_patch(old_state)
        if new_state is None:
            raise Exception("Invalid patch to insert to branch")
        self.states.append(new_state)
        self.patches.append(patch)

    @property
    def curr_state(self):
        return self.states[-1]
