

# returns a tuple of (removed_paths, changed_paths, inserted_paths)
def get_paths(A, B):
    A_keys = set(A.keys())
    B_keys = set(B.keys())

    removed = []
    changed = []
    inserted = []
    for key in A_keys.union(B_keys):
        if key in A_keys and key not in B_keys:
            removed.append([key])
        elif key not in A_keys and key in B_keys:
            inserted.append([key])
        else:
            if isinstance(A[key], dict) and isinstance(B[key], dict):
                # recurse
                removed_paths, changed_paths, inserted_paths = get_paths(A[key], B[key])
                removed.extend([[key] + path for path in removed_paths])
                changed.extend([[key] + path for path in changed_paths])
                inserted.extend([[key] + path for path in inserted_paths])
            else:
                changed.append([key])

    if len(removed) == len(A_keys):
        assert len(inserted) == len(B_keys)
        return [[]], [], [[]]
    elif len(changed) == len(A_keys) and len(inserted) == 0:
        return [], [[]], []

    return removed, changed, inserted