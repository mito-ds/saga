def find_opertations(old, new):
    return _find_operations_rec(old, new, [], [])[0]

def _find_operations_rec(old, new, path, operations):
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
                (operations, path) = _find_operations_rec(old[key], new[key], path, operations)
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

