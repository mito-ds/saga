

class File():

    def __init__(self, file_name):
        self.file_name = file_name

    def get_operations(self, new_file):
        """
        Returns the operations that change self -> new_file
        Hopefully, is as efficient as possible!
        """
        raise NotImplementedError("Must be implemented by child class")

    