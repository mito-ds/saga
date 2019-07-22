from copy import deepcopy
import json
from version_control.file_types.file.File import File
from version_control.file_types.json_file.JSONOpListDelete import JSONOpListDelete
from version_control.file_types.json_file.JSONOpListInsert import JSONOpListInsert
from version_control.file_types.json_file.JSONOpDictAdd import JSONOpDictAdd
from version_control.file_types.json_file.JSONOpDictDelete import JSONOpDictDelete
from version_control.file_types.json_file.JSONOpPrimitiveChange import JSONOpPrimitiveChange
from version_control.file_types.json_file.JSON_utils import get_lcs_indexes, json_equals, PRIMITIVES


class JSONFile(File):

    # A text file is a map from line number to text data
    def __init__(self, file_name, file_contents):
        File.__init__(self, file_name)
        self.file_contents = file_contents

    def get_json_operations(self, path, old_obj, new_obj):
        operations = []
        if type(old_obj) != type(new_obj):
            return []
        elif isinstance(old_obj, dict):
            removed_keys = set(old_obj) - set(new_obj)
            added_keys = set(new_obj) - set(old_obj)
            changed_keys = []
            for key in old_obj:
                if key in new_obj and not json_equals(old_obj[key], new_obj[key]):
                    changed_keys.append(key)

            for key in removed_keys:
                delete_op = JSONOpDictDelete(self.file_name, path + [key])
                operations.append(delete_op)
            for key in added_keys:
                add_op = JSONOpDictAdd(self.file_name, path + [key], deepcopy(new_obj[key]))
                operations.append(add_op)
            for key in changed_keys:
                # we only use change operations on primitive elements
                if type(new_obj[key]) in PRIMITIVES:
                    change_op = JSONOpPrimitiveChange(self.file_name, path + [key], deepcopy(new_obj[key]))
                    operations.append(change_op)
                else:
                    operations += self.get_json_operations(path + [key], old_obj[key], new_obj[key])
        elif isinstance(old_obj, list):
            (lcs_indexes_old, lcs_indexes_new) = get_lcs_indexes(old_obj, new_obj)

            old_idx = 0
            new_idx = 0
            num_deleted = 0
            num_inserted = 0
            while old_idx < len(old_obj) or new_idx < len(new_obj):
                if old_idx not in lcs_indexes_old and old_idx < len(old_obj):
                    delete_op = JSONOpListDelete(self.file_name, path + [str(old_idx - num_deleted + num_inserted)])
                    operations.append(delete_op)
                    num_deleted += 1
                    old_idx += 1
                elif new_idx not in lcs_indexes_new and new_idx < len(new_obj):
                    insert_op = JSONOpListInsert(self.file_name, path + [str(new_idx)], deepcopy(new_obj[new_idx]))
                    operations.append(insert_op)
                    num_inserted += 1
                    new_idx += 1
                else:
                    # should march in unison
                    old_idx += 1
                    new_idx += 1

        return operations

    def get_operations(self, new_file):
        if new_file.file_name != self.file_name:
            raise Exception("Can only get operations on the same files")

        return self.get_json_operations([], self.file_contents, new_file.file_contents)

    def set_path(self, path, new_value):
        curr_obj = self.file_contents
        for step in path[:-1]:
            curr_obj = curr_obj[step]
        curr_obj[path[-1]] = new_value
    
    def delete(self, path):
        curr_obj = self.file_contents
        print(path)
        for step in path[:-1]:
            curr_obj = curr_obj[step]
        if isinstance(curr_obj, list):
            del curr_obj[int(path[-1])]
        else:
            del curr_obj[path[-1]]

    def insert(self, path, new_value):
        curr_obj = self.file_contents
        for step in path[:-1]:
            curr_obj = curr_obj[step]
        idx = int(path[-1])
        curr_obj.insert(idx, new_value)