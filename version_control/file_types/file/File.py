

class File():

    def __init__(self, file_name):
        self.file_name = file_name

    def get_operations(self, new_file):
        """
        Returns the operations that change self -> new_file
        Hopefully, is as efficient as possible!
        """
        raise NotImplementedError("Must be implemented by child class")
    
    def to_string(self):
        """
        Returns a string representing the file
        """
        raise NotImplementedError("Must be implemented by child class")

    @staticmethod
    def from_string(file_string):
        """
        Creates a file object from the string
        """
        raise NotImplementedError("Must be implemented by child class")

    def to_file(self, file_path):
        """
        Writes the file object to the file path (not the string representation)
        """
        raise NotImplementedError("Must be implemented by child class")

    @staticmethod
    def from_file(file_path):
        """
        Writes the file object to the file path (not the string representation)
        """
        raise NotImplementedError("Must be implemented by child class")

    def print_changes(self, new_file):
        """
        Displays the changes that are made between prev and curr version
        """
        raise NotImplementedError("Must be implemented by child class")
