from copy import deepcopy
import json
from version_control.file_types.file.File import File

class JSONFile(File):

    # A text file is a map from line number to text data
    def __init__(self, file_name, file_contents):
        File.__init__(self, file_name)
        self.file_contents = file_contents

    def change(path, new_value)

    def json_equals(obj1, obj2):


    def get_json_operations(self, old_obj, new_obj):
        if type(old_obj) != type(new_obj):
            return []
        elif isinstane(old_obj, dict):
            removed_keys = set(old_obj) - set(new_obj)
            added_keys = set(new_obj) - set(old_obj)
            changed_keys = [key if key in new_obj and json_equals(old_obj[key], new_obj[key]) for key in old_obj]

            
            
            
            in new_obj]


            # get dict difference
            pass
        elid isinstane(old_obj, list):
            # get list difference
            pass


    def get_operations(self, new_file):
        if new_file.file_name != self.file_name:
            raise Exception("Can only get operations on the same files")

        return get_json_operations(old_obj, new_obj)

    def print_changes(self, new_file):
        if new_file.file_name != self.file_name:
            raise Exception("Can only print operations on the same files")

        lcs_indexes_old, lcs_indexes_new = self.get_lcs_indexes(new_file)

        old_idx = 0
        new_idx = 0
        print("File diff: {}".format(self.file_name))
        while old_idx < len(self.file_contents) or new_idx < len(new_file.file_contents):
            # first print all the deletes
            if old_idx not in lcs_indexes_old and old_idx < len(self.file_contents):
                print("- " + self.file_contents[old_idx])
                old_idx += 1
            # then print all inserts
            elif new_idx not in lcs_indexes_new and new_idx < len(new_file.file_contents):
                print("+ " + new_file.file_contents[new_idx])
                new_idx += 1
            else:
                # should march in unison
                assert new_file.file_contents[new_idx] == self.file_contents[old_idx]
                print(self.file_contents[old_idx])
                old_idx += 1
                new_idx += 1

        


    def insert_line(self, line_number, line_contents):
        self.file_contents.insert(line_number, line_contents)

    def delete_line(self, line_number):
        # line numbers are the numbers in the current file
        del self.file_contents[line_number]

    def to_string(self):
        return "JSONFile\t{}\t{}".format(self.file_name, "%".join(json.dumps(self.file_contents)))

    @staticmethod
    def from_string(file_string):
        file_string = file_string.split("\t")
        file_name = file_string[1]
        file_contents = file_string[2].split("%")
        return TextFile(file_name, file_contents)

    def to_file(self, file_path):
        assert file_path.endswith(self.file_name)
        f = open(file_path, "w+")
        f.write("\n".join(self.file_contents))
        f.close()

    @staticmethod
    def from_file(file_path):
        f = open(file_path, "r")
        file_contents = []
        for line in f.readlines():
            if line.endswith("\n"):
                file_contents.append(line[:len(line) - 1])
            else:
                file_contents.append(line)
        return TextFile(file_path, file_contents)