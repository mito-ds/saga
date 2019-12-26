import itertools
from saga.base_file.mixed_data_type.lcs import lcs_with_sim
from saga.base_file.mixed_data_type.diff_utils import dict_removed_paths, dict_inserted_paths, dict_changed_paths

PRIMITIVE = (int, float, bool, str, type(None))

def merge_rec(O, A, B):
    """
    Returns a tuple of (merged object, error).
    If Error = None then the merge was sucessful
    """
    if O is None:
        # this was an add
        if A is None:
            return (B, None)
        if B is None:
            return (A, None)
    else:
        # this was a delete
        if A is None or B is None:
            return (None, None)

    # If one variable is a primitive type, all should be primitive types
    if type(O) in PRIMITIVE or type(A) in PRIMITIVE or type(B) in PRIMITIVE:
        # if a value has been changed in at most one place, then we can merge it
        assert type(O) in PRIMITIVE and type(A) in PRIMITIVE and type(B) in PRIMITIVE
        if O == A and O == B:
            return (O, None)
        elif O != A and O == B:
            return (A, None)
        elif O == A and O != B:
            return (B, None)
        else:
            return (None, True)
    
    # All variables must have the same type!
    assert type(O) == type(A) and type(A) == type(B)

    if type(O) == dict:
        o_a_changed = dict_changed_paths(O, A)
        o_a_inserted = dict_inserted_paths(O, A)
        o_a_removed = dict_removed_paths(O, A)

        o_b_changed = dict_changed_paths(O, B)
        o_b_inserted = dict_inserted_paths(O, B)
        o_b_removed = dict_removed_paths(O, B)

        # if we insert something in both, then we have a merge conflict:
        if any(o_a_inserted.intersection(o_b_inserted)):
            # TODO: we could also not make it a merge conflict, if they add the same thing
            return (None, True)
        # if we removed something from one, and change it in the other
        if any(o_a_removed.intersection(o_b_changed)) or any(o_b_removed.intersection(o_a_changed)):
            return (None, True)

        new_dict = {k: O[k] for k in O}

        # if they were changed in both, we need to merge 
        for changed in o_a_changed.intersection(o_b_changed):
            merged, err = merge_rec(O[changed], A[changed], B[changed])
            if err is not None:
                return (None, True)
            if merged is not None:
                new_dict[changed] = merged

        for removed in o_a_removed.union(o_b_removed):
            del new_dict[removed]
        for a in o_a_changed.union(o_a_inserted).difference(o_b_changed):
            new_dict[a] = A[a]
        for b in o_b_changed.union(o_b_inserted).difference(o_a_changed):
            new_dict[b] = B[b]

        return (new_dict, None)

    elif type(O) == list:
        # we run a modified version of the diff3 algorithm in this case
        matchings_A = bump_matching(lcs_with_sim(A, O))
        matchings_B = bump_matching(lcs_with_sim(B, O))
        chunks = get_chunks(O, A, B, matchings_A, matchings_B)

        calculated_ouput = []

        for chunk_num, chunk in enumerate(chunks):

            ((s_O, e_O), (s_A, e_A), (s_B, e_B)) = chunk

            chunk_in_o = chunk_changed_in_O(chunk, O)
            a_changed = not equal_objs(chunk_in_o, chunk_changed_in_A(chunk, A))
            b_changed = not equal_objs(chunk_in_o, chunk_changed_in_B(chunk, B))
        
            if a_changed and not b_changed:
                calculated_ouput.extend(chunk_changed_in_A(chunk, A))
            elif b_changed and not a_changed:
                calculated_ouput.extend(chunk_changed_in_B(chunk, B))
            else:
                chunk_o, chunk_a, chunk_b = chunk_conflicting_or_stable(chunk, O, A, B)
                if not contains_primitive(chunk_a) \
                    and not contains_primitive(chunk_b) and not contains_primitive(chunk_o):
                    # There's a "location" of these sublist elements in the final list, and then there's the combining
                    # of the sublists when they are equal... 

                    # TODO: not sure about this condition
                    if len(chunk_a) > len(chunk_o) and len(chunk_b) > len(chunk_o):
                        # ignore nones!

                        overlay = none_overlay(chunk_a, chunk_b)
                        print(f"OVERLAY {overlay}")
                        if overlay is not None:
                            calculated_ouput.extend(overlay)
                            continue
                        else:
                            return (None, True)
        
                    for o, a, b in itertools.zip_longest(chunk_o, chunk_a, chunk_b):
                        rec_merge, err = merge_rec(o, a, b)
                        if err is not None:
                            return (None, True)
                        if rec_merge is not None:
                            calculated_ouput.append(rec_merge)  

                else:
                    # have to check none overlap here, too
                    overlay = none_overlay_primitive(chunk_a, chunk_b)
                    if overlay is None:
                        return (None, True)

                    calculated_ouput.extend(overlay)

        return (calculated_ouput, None)
    else:
        raise ValueError("Invalid type given to merge: {}".format(type(O)))

# utilities for diff3

def none_overlay(matrix_a, matrix_b):
    
    # overlays 2 2-d arrays, where None is treated as a blank space
    overlay = []
    for a, b in itertools.zip_longest(matrix_a, matrix_b):
        if a == None:
            overlay.append(b)
        elif b == None:
            overlay.append(a)
        else:
            overlay.append([])
            idx = len(overlay) - 1
            for x, y in itertools.zip_longest(a, b):
                if x == y:
                    overlay[idx].append(x)
                elif x == None:
                    overlay[idx].append(y)
                elif y == None:
                    overlay[idx].append(x)
                else:
                    return None
    return overlay

def none_overlay_primitive(list_a, list_b):
    import itertools
    # overlays 2 2-d arrays, where None is treated as a blank space
    overlay = []
    for a, b in itertools.zip_longest(list_a, list_b):
        if a == b:
            overlay.append(a)
        elif a == None:
            overlay.append(b)
        elif b == None:
            overlay.append(a)
        else:
            return None
    return overlay

def bump_matching(matching):
    new_matchings = []
    for path1, path2, sim in matching:
        path1 = [i + 1 for i in path1]
        path2 = [i + 1 for i in path2]
        new_matchings.append((path1, path2, sim))
    return new_matchings


def get_chunks(O, A, B, matchings_A, matchings_B):
    chunks = []
    idx_A, idx_O, idx_B = 0, 0, 0
    max_idx_A, max_idx_O, max_idx_B = len(A), len(O), len(B)

    i = 1
    # we keep trying to make chunks while we haven't run off the end of any list
    while not (i + idx_A > max_idx_A or i + idx_O > max_idx_O or i + idx_B > max_idx_B):
        # if there is no longer a matching between these indicies
        if not is_matching(matchings_A, idx_A + i, idx_O + i) or not is_matching(matchings_B, idx_B + i, idx_O + i):
            # and i is 1 
            if i == 1:
                # then we find the end index of the unstable chunk (e.g. while it remains stable)
                found = False
                for j in range(idx_O + 1, max_idx_O + 1):
                    last_indexes = is_stable_index(matchings_A, matchings_B, j)
                    if last_indexes:
                        found = True
                        # found last index of unstable chunk
                        (end_A, end_O, end_B) = last_indexes
                        unstable_chunk = ((idx_O + 1, end_O - 1), (idx_A + 1, end_A - 1), (idx_B + 1, end_B - 1))
                        chunks.append(unstable_chunk)
                        idx_A, idx_O, idx_B = end_A - 1, end_O - 1, end_B - 1
                        i = 1
                        break
                # thus, there is no matchings, and so we output one more final chunk
                if not found:
                    unstable_chunk = ((idx_O + 1, max_idx_O), (idx_A + 1, max_idx_A), (idx_B + 1, max_idx_B))
                    chunks.append(unstable_chunk)
                    return chunks
            # otherwise, this is a stable chunk, and we just output it
            else:
                stable_chunk = ((idx_O + 1, idx_O + i - 1), (idx_A + 1, idx_A + i - 1), (idx_B + 1, idx_B + i - 1))
                chunks.append(stable_chunk)
                idx_A, idx_O, idx_B = idx_A + i - 1, idx_O + i - 1, idx_B + i - 1
                i = 1
        else:
            i += 1
    else:
        # we made one final chunk
        last_chunk = ((idx_O + 1, max_idx_O), (idx_A + 1, max_idx_A), (idx_B + 1, max_idx_B))
        chunks.append(last_chunk)
        return chunks

def contains_primitive(l):
    return len(l) > 0 and type(l[0]) in PRIMITIVE 

def chunk_changed_in_O(chunk, O):
    #output A[H], A[H], A[H]
    ((s_O, e_O), _, _) = chunk
    return O[s_O - 1 : e_O]   

def chunk_changed_in_A(chunk, A):
    #output A[H], A[H], A[H]
    (_, (s_A, e_A), _) = chunk
    return A[s_A - 1 : e_A]

def chunk_changed_in_B(chunk, B):
    #output B[H], B[H], B[H]
    (_, _, (s_B, e_B)) = chunk
    return B[s_B - 1 : e_B]

def chunk_conflicting_or_stable(chunk, O, A, B):
    #output A[H], O[H], B[H]
    ((s_O, e_O), (s_A, e_A), (s_B, e_B)) = chunk
    return (O[s_O - 1: e_O ], A[s_A - 1: e_A], B[s_B - 1: e_B ])

def chunk_changed(matchings, s, e, s_O, e_O):
    for i in range (s, e + 1):
            if matched(matchings, i) != 1:
                return True

    for i in range (s_O, e_O + 1):
            if matched_O(matchings, i) != 1:
                return True

    return False

# returns true if a matching exists with this index of A or B
def matched(matchings, idx):
    for match in matchings:
        ([i], _, sim) = match
        if (i == idx):
            return sim 
    return 0

# returns true if a matching exists with this index of A or B
def matched_O(matchings, idx):
    for match in matchings:
        (_, [i], sim) = match
        if (i == idx):
            return sim
    return 0

# i is matched to j
def is_matching(matchings, i, j):
    for match in matchings:
        (i_prime, j_prime, similarity) = match
        if i == i_prime[0] and j == j_prime[0]:
            return True
    return False

def is_stable_index(matchings_A, matchings_B, idx_O):
    for match_A in matchings_A:
        if match_A[1][0] == idx_O:
            for match_B in matchings_B:
                if match_B[1][0] == idx_O:
                    # return (idx_A, idx_O, idx_B)
                    return (match_A[0][0], match_A[1][0], match_B[0][0])
    return False 


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
        if len(a.keys()) != len(b.keys()) or \
            any(set(a.keys()).symmetric_difference(set(b.keys()))):
            return False
        for key in a.keys():
            if not equal_objs(a[key], b[key]):
                return False
        return True

    raise ValueError(f"Passed invalid type of {type(a)}")