from version_control.file.OPFileChangeName import OPFileChangeName

class File(object):

    def __init__(self, file_id, file_type, file_name, file_contents):
        """
        Create a new representation of a file:
            - file_id, file_type are static and can never change
            - file_name, file_contents can
        """
        self.file_id = file_id
        self.file_type = file_type
        self.file_name = file_name
        self.file_contents = file_contents


    def get_operations(self, other_file):
        """
        Get the operations between this file and other_file, which is thought of as the new
        version of the file. 
        """
        if self.file_id != other_file.file_id:
            raise ValueError("Can only get operations between different versions of the same file")

        operations = []
        if self.file_name != other_file.file_name:
            operations.append(OPFileChangeName(self.file_id, self.file_name, other_file.file_name))

        # now we delegate the operations to the file_contents
        operations.extend(self.file_contents.get_operations(other_file.file_contents))
        return operations

    
