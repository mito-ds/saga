
class State():

    def __init__(self, files):
        # map from file id -> contents
        self.files = files 

    def __contains__(self, file_name):
        return file_name in self.files
