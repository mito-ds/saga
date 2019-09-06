from saga.State import State

class Branch():

    def __init__(self):
        self.patches = []
        # Set the initial state to be the empty state
        self.states = [State(dict(), None)]

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


    def least_common_ancestor(self, other_branch):
        for state in reversed(self.states):
            for other_state in reversed(other_branch.states):
                if state.get_hash() == other_state.get_hash():
                    return state
        return None


