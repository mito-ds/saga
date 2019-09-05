
class State():

    def __init__(self, files):
        # map from file_id -> file object
        self.files = files 

    def __getitem__(self, file_id):
        return self.files.get(file_id, None) # we return None of the file does not exist

    def __setitem__(self, file_id, file):
        self.files[file_id] = file

    def __contains__(self, file_name):
        return file_name in self.files

    def __len__(self):
        return sum(1 for file_id in self.files if self.files[file_id] is not None)
