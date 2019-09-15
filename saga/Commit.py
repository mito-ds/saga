import pickle
import hashlib

class Commit(object):

    def __init__(self, state_hash, parent_commit_hashes, commit_message):
        self.state_hash = state_hash
        self.parent_commit_hashes = parent_commit_hashes
        self.commit_message = commit_message

    def hash(self):
        m = hashlib.sha256()
        m.update(self.to_bytes())
        return m.hexdigest()
    
    def to_bytes(self):
        return pickle.dumps(self)

    @staticmethod
    def from_bytes(commit_bytes):
        return pickle.loads(commit_bytes)


