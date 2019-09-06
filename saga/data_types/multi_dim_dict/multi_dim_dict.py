from saga.data_types.multi_dim_dict.path_utils import get_paths
from saga.data_types.multi_dim_dict.OP_MDD_Change import OP_MDD_Change
from saga.data_types.multi_dim_dict.OP_MDD_Insert import OP_MDD_Insert
from saga.data_types.multi_dim_dict.OP_MDD_Remove import OP_MDD_Remove

def value_at_path(dictonary, path):
    if len(path) == 0:
        return dictonary
    else:
        return value_at_path(dictonary[path[0]], path[1:])


class MultiDimDict(object):

    def __init__(self, dictonary):
        self.dictonary = dictonary

    def get_operations(self, dict_object):
        A = self.dictonary
        B = dict_object.dictonary

        removed_paths, changed_paths, inserted_paths = get_paths(A, B)

        operations = []
        for removed in removed_paths:
            operations.append(OP_MDD_Remove("temp", removed, value_at_path(A, removed)))

        for changed in changed_paths:
            operations.append(OP_MDD_Change("temp", changed, value_at_path(A, changed), value_at_path(B, changed)))

        for inserted in inserted_paths:
            operations.append(OP_MDD_Insert("temp", inserted, value_at_path(B, inserted)))

        return operations

        



        