def value_at_path(obj, path):
    if len(path) == 0:
        return obj
    else:
        return value_at_path(obj[path[0]], path[1:])

def dict_same_paths(dict_a, dict_b):
    return {k for k in dict_a if k in dict_b and dict_a[k] == dict_b[k]}

def dict_removed_paths(dict_a, dict_b):
    return set(dict_a.keys()).difference(dict_b.keys())

def dict_inserted_paths(dict_a, dict_b):
    return removed_paths(dict_b, dict_a)

def dict_changed_paths(dict_a, dict_b):
    return {k for k in dict_a if k in dict_b and dict_a[k] != dict_b[k]}

class MixedDataType(object):

    def __init__(self, mixed_data_type):
        self.mixed_data_type = mixed_data_type

    def get_operations(self, mixed_data_type_obj):
        return []
        """
        A = self.multi_dim_list
        B = mixed_data_type_obj.mixed_data_type

        if type(A) != type(B):
            raise Exception("Type tree cannot change! {} is not {}".format(type(A), type(B)))

        if type(A) == dict:

        elif type(B) == list:


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
        """

    def merge(self, a_mdt, b_mdt):
        O = self.mixed_data_type
        A = a_mdt.mixed_data_type
        B = b_mdt.mixed_data_type

        return MixedDataType(merge_rec(O, A, B))


    