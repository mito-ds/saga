from saga.base_file.mixed_data_type.lcs import lcs_with_sim

PRIMITIVE = (int, float, bool, str)

def paths(A, B):
    # returns a triple (removed_paths, changed_paths, inserted_paths)
    if type(A) in PRIMITIVE or type(B) in PRIMITIVE:
        assert type(A) in PRIMITIVE and type(B) in PRIMITIVE
        return [], [], [] if A == B else [], [[]], []

def changed_paths(A, B):
    return _changed_paths(A, B, [])

def _changed_paths(A, B, base_path):
    if type(A) in PRIMITIVE or type(B) in PRIMITIVE:
        assert type(A) in PRIMITIVE and type(B) in PRIMITIVE
        return [] if A == B else [base_path]

    # All variables must have the same type!
    assert type(A) == type(B)

    changed_paths = []
    
    if type(A) == dict:
        changed_keys = dict_changed_paths(A, B)

        # we only report changes on the lowest level
        for key in changed_keys:
            changed_paths.extend(_changed_paths(A[key], B[key], base_path + [key]))
        
        return changed_paths

    elif type(A) == list:
        lcs = lcs_with_sim(A, B)
        count = 0
        for path_a, path_b, sim in lcs:
            if sim < 1:
                count += 1
                changed_paths.extend(_changed_paths(A[path_a[0]], B[path_b[0]], base_path + path_a))
        if count == len(A) and count > 0 and len(base_path) > 0:
            # the whole list was changed, and so we just say this list was changed
            return [base_path]

        return changed_paths
    else:
        raise ValueError("Error: unknown type given: {}".format(type(A)))
    
def removed_paths(A, B):
    return _removed_paths(A, B, [])

def _removed_paths(A, B, base_path):
    if type(A) in PRIMITIVE or type(B) in PRIMITIVE:
        return []

    # All variables must have the same type!
    assert type(A) == type(B)

    if type(A) == dict:
        removed = []
        removed_keys = dict_removed_paths(A, B)
        # if the whole dictonary has been changed we report that
        if len(removed_keys) == len(A) and len(A) > 0:
            return [base_path]
        # otherwise
        removed.extend([base_path + [key] for key in removed_keys])

        # we also have to recurse on all the changed paths
        changed_keys = dict_changed_paths(A, B)
        for key in changed_keys:
            removed.extend(_removed_paths(A[key], B[key], base_path + [key]))
        
        # we don't recurse, as it doesn't matter what happened below
        return removed

    elif type(A) == list:
        removed_paths = []
        lcs = lcs_with_sim(A, B)
        # nothing was matched, so we removed all the objects
        # but if nothing was matched as it was empty, then it wasn't deleted
        if len(lcs) == 0 and len(A) > 0 and len(base_path) > 0:
            return [base_path]

        for idx in range(len(A)):
            matched = False
            for [idx_a], [idx_b], sim in lcs:
                if idx == idx_a:
                    matched = True
                    break
            if not matched:
                removed_paths.append(base_path + [idx])
            elif matched and sim < 1:
                # if the subtype of the list is not primitive, we have to recurse here also
                if type(A[idx]) not in PRIMITIVE:
                    removed_paths.extend(_removed_paths(A[idx], B[idx_b], base_path + [idx]))

                # we have to recurse

        return removed_paths
    else:
        raise ValueError("Error: unknown type given: {}".format(type(A)))

def inserted_paths(A, B):
    return removed_paths(B, A)

def dict_removed_paths(dict_a, dict_b):
    return set(dict_a.keys()).difference(dict_b.keys())

def dict_inserted_paths(dict_a, dict_b):
    return dict_removed_paths(dict_b, dict_a)

def dict_changed_paths(dict_a, dict_b):
    return {k for k in dict_a if k in dict_b and dict_a[k] != dict_b[k]}


