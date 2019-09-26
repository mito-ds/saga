from saga.data_types.multi_dim_dict.OP_MDD_Change import OP_MDD_Change
from saga.data_types.multi_dim_dict.OP_MDD_Insert import OP_MDD_Insert
from saga.data_types.multi_dim_dict.OP_MDD_Remove import OP_MDD_Remove


def value_at_path(arr, path):
    if len(path) == 0:
        return arr
    if len(path) == 1:
        return [arr[path[0]]]
    elif path[0] == "_":
        values = []
        for sublist in arr:
            values.extend(value_at_path(sublist, path[1:]))
        return values
    else:
        return value_at_path(arr[path[0]], path[1:])
    

class MultiDimDict(object):

    def __init__(self, multi_dim_dict, dimension):
        self.multi_dim_dict = multi_dim_dict
        self.dimension = dimension

    def remove_path(self, path):
        self._remove_path_rec(self.multi_dim_dict, path)

    def _remove_path_rec(self, arr, path):
        if len(path) == 0:
            arr.clear()
            return
        if len(path) == 1:
            del arr[path[0]]
        elif path[0] == "_":
            for sublist in arr:
                self._remove_path_rec(sublist, path[1:])
        else:
            self._remove_path_rec(arr[path[0]], path[1:])
        
    def insert_path(self, path, value):
        self.multi_dim_dict = self._insert_path_rec(self.multi_dim_dict, path, value) 

    def _insert_path_rec(self, arr, path, value):
        if len(path) == 0:
            arr.update(value)
            return arr
        else:
            arr[path[0]] = self._insert_path_rec(arr[path[0]], path[1:], value)
        return arr

    def change_value(self, path, value):
        self._change_value_rec(self.multi_dim_dict, path, value)

    def _change_value_rec(self, arr, path, value):
        if len(path) == 1:
            arr[path[0]] = value
        else:
            self._change_value_rec(arr[path[0]], path[1:], value)

    def get_operations(self, multi_dim_obj):
        new_file = self.multi_dim_dict
        old_file = multi_dim_obj.multi_dim_dict

        operations = self._find_operations_rec(old_file, new_file, [], [])[0]
        return operations


    def _find_operations_rec(self, old, new, path, operations):
        old_type, new_type = type(new), type(old)

        # if both old and new are dictionaries
        if old_type == dict and new_type == dict:
            all_keys, all_unique_keys = [], []
            all_keys.extend(new.keys())
            all_keys.extend(old.keys())

            for key in all_keys:
                if not key in all_unique_keys:
                    all_unique_keys.append(key)

            for key in all_unique_keys:
                if key in new.keys() and not key in old.keys():
                    operations.append(OP_MDD_Insert("id", path, {key : new[key]}))
                elif key in old.keys() and key not in new.keys():
                    path.append(key)
                    operations.append(OP_MDD_Remove("id", path, {key : old[key]}))
                    path = path[:-1]
                else:
                    path.append(key)
                    (operations, path) = self._find_operations_rec(old[key], new[key], path, operations)
            path = path[:-1]        
            return (operations, path)

        # if neither are dictionaries
        if not old_type == dict and not new_type == dict:
            # change of value
            if not old == new:
                # value changed 
                operations.append(OP_MDD_Change("id", path, old, new))
                path = path[:-1]
                return (operations, path)
            # no change
            else:
                path = path[:-1]
                return (operations, path)

        # if one is a dictionary
        else: 
            operations.append(OP_MDD_Change("id", path, old, new))
            path = path[:-1]
            return (operations, path)
    