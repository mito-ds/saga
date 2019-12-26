from saga.base_file.mixed_data_type.merge_utils import merge_rec, equal_objs
from saga.base_file.mixed_data_type.diff_utils import inserted_paths, removed_paths, changed_paths

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
        A =  self.mixed_data_type
        B = mixed_data_type_obj.mixed_data_type

        removed = removed_paths(A, B)
        changed = changed_paths(A, B)
        inserted = inserted_paths(A, B)

        return {"removed": removed, "changed": changed, "inserted": inserted}

    def merge(self, a_mdt, b_mdt):
        O = self.mixed_data_type
        A = a_mdt.mixed_data_type
        B = b_mdt.mixed_data_type

        merged, err = merge_rec(O, A, B)
        return MixedDataType(merged)

    def __eq__(self, value):
        if not isinstance(value, MixedDataType):
            return False
        return equal_objs(self.mixed_data_type, value.mixed_data_type)

PRIMITIVE = (int, float, bool, str, type(None))

    