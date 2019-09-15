from saga.data_types.multi_dim_list.lcs import changed_paths, inserted_paths, removed_paths, lcs_multi_dimension, get_matching_path
from saga.data_types.multi_dim_list.OP_MDL_Change import OP_MDL_Change
from saga.data_types.multi_dim_list.OP_MDL_Insert import OP_MDL_Insert
from saga.data_types.multi_dim_list.OP_MDL_Remove import OP_MDL_Remove
from saga.data_types.multi_dim_list.mdl_merge_utils import diff3

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
    

class MultiDimList(object):

    def __init__(self, multi_dim_list, dimension):
        self.multi_dim_list = multi_dim_list
        self.dimension = dimension

    def remove_path(self, path):
        self._remove_path_rec(self.multi_dim_list, path)

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
        self.multi_dim_list = self._insert_path_rec(self.multi_dim_list, path, value) 

    def _insert_path_rec(self, arr, path, value):
        if len(path) == 0:
            return value

        if len(path) == 1:
            arr.insert(path[0], value[0])
        elif path[0] == "_":
            step = int(len(value) / len(arr)) 
            for idx, sublist in enumerate(arr):
                arr[idx] = self._insert_path_rec(sublist, path[1:], value[idx * step: idx * step + step])
        else:
            arr[path[0]] = self._insert_path_rec(arr[path[0]], path[1:], value)
        
        return arr

    def change_value(self, path, value):
        self._change_value_rec(self.multi_dim_list, path, value)

    def _change_value_rec(self, arr, path, value):
        if len(path) == 1:
            arr[path[0]] = value
        else:
            self._change_value_rec(arr[path[0]], path[1:], value)

    def get_operations(self, multi_dim_obj):
        A = self.multi_dim_list
        B = multi_dim_obj.multi_dim_list

        dimension_matches = lcs_multi_dimension(A, B, self.dimension)

        operations = []

        removed_rows, removed_cols = removed_paths(A, B, dimension_matches)
        for path in removed_rows + removed_cols:
            operations.append(OP_MDL_Remove("id", path, value_at_path(A, path)))

        inserted_rows, inserted_cols = inserted_paths(A, B, dimension_matches)
        for path in inserted_rows + inserted_cols:
            operations.append(OP_MDL_Insert("id", path, value_at_path(B, path)))

        changed = changed_paths(A, B, dimension_matches)
        for path in changed:
            a_path, _ = get_matching_path(dimension_matches, False, path)
            operations.append(OP_MDL_Change("id", path, value_at_path(A, a_path), value_at_path(B, path)))
        
        return operations

    def merge(self, a_mdl, b_mdl):
        merge_res = diff3(a_mdl.multi_dim_list, self.multi_dim_list, b_mdl.multi_dim_list)
        if merge_res is None:
            return None

        return MultiDimList(merge_res, self.dimension)

    