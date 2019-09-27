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
    

def same_paths(dict_a, dict_b):
    return {k for k in dict_a if k in dict_b and dict_a[k] == dict_b[k]}

def removed_paths(dict_a, dict_b):
    return set(dict_a.keys()).difference(dict_b.keys())

def inserted_paths(dict_a, dict_b):
    return removed_paths(dict_b, dict_a)

def changed_paths(dict_a, dict_b):
    return {k for k in dict_a if k in dict_b and dict_a[k] != dict_b[k]}

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

    def merge(self, a_mdd, b_mdd):
        O = self.multi_dim_dict
        A = a_mdd.multi_dim_dict
        B = b_mdd.multi_dim_dict

        o_a_changed = changed_paths(O, A)
        o_a_inserted = inserted_paths(O, A)
        o_a_removed = removed_paths(O, A)

        o_b_changed = changed_paths(O, B)
        o_b_inserted = inserted_paths(O, B)
        o_b_removed = removed_paths(O, B)

        # if we insert something in both, then we have a merge conflict:
        if any(o_a_inserted.intersection(o_b_inserted)):
            # TODO: we could also not make it a merge conflict, if they add the same thing
            return None
        # if we removed something from one, and change it in the other
        if any(o_a_removed.intersection(o_b_changed)) or any(o_b_removed.intersection(o_a_changed)):
            return None
        # if they were changed in both, we have a merge conflict:
        if any(o_a_changed.intersection(o_b_changed)):
            return None

        # TODO: we can probably just avoid the above checking by keep track of what keys are changed
        new_dict = {k: O[k] for k in O}
        for removed in o_a_removed.union(o_b_removed):
            del new_dict[removed]
        for a in o_a_changed.union(o_a_inserted):
            new_dict[a] = A[a]
        for b in o_b_changed.union(o_b_inserted):
            new_dict[b] = B[b]

        return MultiDimDict(new_dict, self.dimension)
    