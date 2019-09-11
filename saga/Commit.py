import pickle
import hashlib

class Commit(object):

    def __init__(self, state_hash, parent_commit_hashes):
        self.state_hash = state_hash
        self.parent_commit_hashes = parent_commit_hashes

    def hash(self):
        m = hashlib.sha256()
        m.update(bytearray(self.to_string()))
        return m.hexdigest()
    
    def to_string(self):
        return pickle.dumps(self)

    @staticmethod
    def from_string(commit_string):
        return pickle.loads(commit_string)
