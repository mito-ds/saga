from copy import deepcopy
import json
from version_control.file_types.file.File import File
from version_control.file_types.text_file.text_utils import lcs
from version_control.file_types.json_file.JSONOpDelete import JSONOpDelete
from version_control.file_types.json_file.JSONOpInsert import JSONOpInsert
from version_control.file_types.json_file.JSON_utils import get_lcs_indexes, json_equals, PRIMITIVES


class JSONFile(File):

    # A text file is a map from line number to text data
    def __init__(self, file_name, file_contents):
        File.__init__(self, file_name)
        self.file_contents = file_contents

    def get_path_and_types(self, obj_arr):
        assert obj_arr[0] == "{" and obj_arr[-1] == "}" # must be valid JSON
        path_and_types = [None]
        path_stack = []
        type_stack = []

        for line in obj_arr[1:-1]:
            print("LINE: {}".format(line))
            if line.endswith("{"):
                type_stack.append("dict")
                path_stack.append(line.split(":")[0][1:-1])
            elif line.endswith("}") or line.endswith("]"):
                type_stack.pop(-1)
                path_stack.pop(-1)
            elif line.endswith("["):
                type_stack.append("list")
                path_stack.append(line.split(":")[0][1:-1])
            print("PATH STACK {}".format(path_stack))
            print("TYPE STACK {}".format(type_stack))
            if not any(path_stack) or not any(type_stack):
                return path_and_types

            path_and_type = [path_stack[-1], type_stack[-1]]
            path_and_types.append(path_and_type)
        return path_and_types


    def get_json_operations(self, old_obj, new_obj):
        # We can take each operation, turn it into a string
        # Then split it into a list of lines, and then do an LCS on this
        # This has the benefit of being stable when objects are nested or unnested,
        # and the disadvantage of being slow as shit. 
        old_obj_arr = [s.strip() for s in json.dumps(old_obj, indent=4, sort_keys=True).split("\n")]
        new_obj_arr = [s.strip() for s in json.dumps(new_obj, indent=4, sort_keys=True).split("\n")]

        # This is the type of json object at that index in the old_obj_arr or new_obj_arry
        old_path_and_types = self.get_path_and_types(old_obj_arr)
        new_path_and_types = self.get_path_and_types(new_obj_arr)

        print(old_obj_arr)
        print(old_path_and_types)
        print(new_obj_arr)
        print(new_path_and_types)

        lcs_indexes_old, lcs_indexes_new = lcs(self.file_contents, new_file.file_contents)

        delete_patches = []
        for line_number in range(len(old_obj_arr)):
            if line_number not in lcs_indexes_old:
                relative_line_num = line_number - len(delete_patches) # get the relative number, accounting for lines deleted before
                delete_patches.append(TextOpDeleteLine(self.file_name, relative_line_num))

        insert_patches = []
        for line_number in range(len(new_file.file_contents)):
            if line_number not in lcs_indexes_new:
                insert_patches.append(TextOpInsertLine(self.file_name, line_number, new_file.file_contents[line_number]))

        return delete_patches + insert_patches
        



        

    def get_operations(self, new_file):
        if new_file.file_name != self.file_name:
            raise Exception("Can only get operations on the same files")

        return self.get_json_operations(self.file_contents, new_file.file_contents)
    
    def delete(self, path):
        curr_obj = self.file_contents
        print(path)
        for step in path[:-1]:
            curr_obj = curr_obj[step]
        if isinstance(curr_obj, list):
            del curr_obj[int(path[-1])]
        else:
            del curr_obj[path[-1]]

    def insert(self, path, new_value, move_list):
        curr_obj = self.file_contents
        for step in path[:-1]:
            curr_obj = curr_obj[step]
        if isinstance(curr_obj, list):
            idx = int(path[-1])
            if move_list:
                curr_obj.insert(idx, new_value)
            else:
                curr_obj[idx] = new_value
        else:
            curr_obj[path[-1]] = new_value