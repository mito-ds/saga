from saga.base_file.mixed_data_type.merge_utils import merge_rec
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

        return MixedDataType(merge_rec(O, A, B))

    def __eq__(self, value):
        if not isinstance(value, MixedDataType):
            return False
        return equal_objs(self.mixed_data_type, value.mixed_data_type)

PRIMITIVE = (int, float, bool, str, type(None))

def equal_objs(a, b):
    if type(a) != type(b):
        return False

    if type(a) in PRIMITIVE:
        return a == b
    
    if isinstance(a, list):
        if len(a) != len(b):
            return False
        for x, y in zip(a, b):
            if not equal_objs(x, y):
                return False
        return True

    if isinstance(a, dict):
        if len(a.keys()) != len(b.keys()) or any(a.keys().symmetric_difference(b.keys())):
            return False
        for key in a.keys():
            if not equal_objs(a[key], b[key]):
                return False
        return True

    raise ValueError(f"Passed invalid type of {type(a)}")
    