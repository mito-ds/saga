
class State():

    def __init__(self, files):
        # map from file_id -> file object
        self.files = files 

    def __getitem__(self, file_id):
        return self.files[file_id]

    def __setitem__(self, file_id, file):
        self.files[file_id] = file

    def __contains__(self, file_name):
        return file_name in self.files
