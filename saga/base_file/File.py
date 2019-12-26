from saga.base_file.mixed_data_type.MixedDataType import MixedDataType

class File(object):

    def __init__(self, file_id, file_type, file_path, file_name, file_contents):
        """
        Create a new representation of a file:
            - file_id, file_type are static and can never change
            - file_name, file_contents can
        """
        self.file_id = file_id
        self.file_type = file_type
        self.file_path = file_path
        self.file_name = file_name
        self.file_contents = MixedDataType(file_contents)

    def get_operations(self, other_file):
        """
        Get the operations between this file and the new version of the file, other_file
        """
        if self.file_id != other_file.file_id:
            raise ValueError("Can only get operations between different versions of the same file")

        operations = {"file": []}
        if self.file_name != other_file.file_name:
            operations["file"].append("Change file name from {} to {}".format(self.file_name, other_file.file_name))

        # now we delegate the operations to the file_contents
        operations.update(self.file_contents.get_operations(other_file.file_contents))
        return operations

    # this should be called on the origin file
    def merge(self, file_a, file_b, file_path=None):
        merge_res = self.file_contents.merge(file_a.file_contents, file_b.file_contents)
        if merge_res is None:
            return None
        return File(self.file_id, self.file_type, file_path, self.file_name, merge_res.mixed_data_type)
