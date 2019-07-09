

class State():

    def __init__(self, files):
        # map from file id -> contents
        self.files = files 

class Operation():

    def __init__(self, name):
        self.name = name

    def apply_operation(self, state):
        # Returns an option: 
            # Some (new state) if operation can be applied
            # None if the operation cannot be applied
        pass

class AddFileOperation(Operation):

    def __init__(self, new_file):
        

    def valid_oper



class Patch():

    def __init__(self, operations):
        self.operations = operations # set of operation objects

    def apply_patch(self, state):
        # TODO: returns new state, by applying each operation in the
        # patch. I actually think this is very monadic, lol.

    
class Branch():

    def 



# Linear history of patches; each patch is immutable, and says what it changes
class Patch():
    def __init__(self, parent_patch, changes):
        self.parent_patch = parent_patch
        # map from fileid -> change (for now, only add a line with some text)
        self.changes = changes

    def is_ancestor_patch(self, patch):
        curr_patch = self
        while curr_patch is not None:
            if curr_patch == patch:
                return True
            curr_patch = curr_patch.parent_patch
        
        return False
        
    def least_common_ancestor(self, patch):
        # walk back parent patches
        curr_patch = self

        while curr_patch and not curr_patch.is_ancestor_patch(patch)
            curr_patch = curr_patch.parent_patch
        
        return curr_patch

class Repository():
    def __init__(self):
        self.patches = []

    def most_recent(self):
        

    def add_patch(self, new_patch):
        # TODO: make sure the patch actually can be applied
        self.patches.add(new_patch)

    def merge(self, repository):
        # find common ancestor
