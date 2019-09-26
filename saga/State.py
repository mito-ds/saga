import pickle
import hashlib

class State():

    def __init__(self, files, prev_state_hash):
        # map from file_id -> file object
        self.files = files 
        self.prev_state_hash = prev_state_hash

    def __getitem__(self, file_id):
        return self.files.get(file_id, None) # we return None of the file does not exist

    def __setitem__(self, file_id, file):
        self.files[file_id] = file

    def __contains__(self, file_name):
        return file_name in self.files

    def __len__(self):
        return sum(1 for file_id in self.files if self.files[file_id] is not None)

    def get_hash(self):
        m = hashlib.sha256()
        m.update(bytearray(self.to_string()))
        return m.hexdigest()

    def to_string(self):
        return pickle.dumps(self)

    def from_string(self, str):
        return pickle.loads(str)

    


    
