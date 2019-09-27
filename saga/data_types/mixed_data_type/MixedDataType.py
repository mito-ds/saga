from saga.data_types.multi_dim_list.lcs import changed_paths, inserted_paths, removed_paths, lcs_multi_dimension, get_matching_path
from saga.data_types.multi_dim_list.OP_MDL_Change import OP_MDL_Change
from saga.data_types.multi_dim_list.OP_MDL_Insert import OP_MDL_Insert
from saga.data_types.multi_dim_list.OP_MDL_Remove import OP_MDL_Remove
from saga.data_types.multi_dim_list.mdl_merge_utils import diff3

def value_at_path(obj, path):
    if len(path) == 0:
        return obj
    else:
        return value_at_path(obj[path[0]], path[1:])

class MixedDataType(object):

    def __init__(self, mixed_data_type):
        """
        A mixed_data_type is a list or a dictionary. If the object is a list, it 
        must contain only one type beneath it. If it is a dictonary, it can contain mulitple
        types? 

        """
        self.mixed_data_type = mixed_data_type

    def get_operations(self, mixed_data_type_obj):
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

    def merge(self, a_mdt, b_mdt):
        


        merge_res = diff3(a_mdl.multi_dim_list, self.multi_dim_list, b_mdl.multi_dim_list, self.dimension)
        if merge_res is None:
            return None

        return MultiDimList(merge_res, self.dimension)

    