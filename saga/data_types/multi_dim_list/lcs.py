"""
A set of functions for computing longest-common subsequences between lists.
"""
from copy import deepcopy


# Standard LCS
def lcs(A, B):
    def equal(a, b):
        if a == b:
            return 1
        return 0

    return lcs_similarity(A, B, equal)

# LCS with a similarity function. 
def lcs_similarity(A, B, similarity_function):
    m = len(A) 
    n = len(B) 

    # L[i][j] is the highest similar metric of the close longest common subsequece up to indexes i, j
    L = [[None]*(n + 1) for i in range(m + 1)] 
    for i in range(m + 1): 
        for j in range(n + 1): 
            if i == 0 or j == 0 : 
                L[i][j] = 0
            else:
                L[i][j] = max(
                    similarity_function(A[i - 1], B[j - 1]) + L[i - 1][j - 1],
                    L[i - 1][j],
                    L[i][j - 1]
                )

    # Create an array to store indexes of close common subsequence
    matches = []

    # Start from the right-most-bottom-most corner and 
    # one by one store characters in lcs[] 
    i = m 
    j = n 
    while i > 0 and j > 0:

        # If current character in X[] and Y are same, then 
        # current character is part of LCS 
        if similarity_function(A[i - 1], B[j - 1]) + L[i - 1][j - 1] > max(L[i - 1][j], L[i][j - 1]): 
            matches.append(([i - 1], [j - 1], similarity_function(A[i - 1], B[j - 1])))
            i-=1
            j-=1

        # If not same, then find the larger of two and 
        # go in the direction of larger value 
        elif L[i-1][j] > L[i][j-1]:
            i-=1
        else: 
            j-=1

    return matches


def arr_equals(A, B):
    if len(A) != len(B):
        return False
    if type(A) in (int, float, bool, str) and type(B) in (int, float, bool, str):
        return A == B
    for a, b in zip(A, B):
        if not arr_equals(a, b):
            return False
    return True

def list_from_path(matrix, path):
    curr = matrix
    for step in path:
        curr = curr[step]
    return curr

def list_similiarity_function(A, B):
    if type(A) in (int, float, bool) and type(B) in (int, float, bool):
        if A == B:
            return 1
        else:
            return 0
    elif len(A) == 0 and len(B) == 0:
        return 1
    elif type(A) == str and type(B) == str:
        indexes = lcs(A, B)
        if any(indexes):
            return len(indexes) / max(len(A), len(B))
        return 0

    indexes = lcs_similarity(A, B, list_similiarity_function)
    if any(indexes):
        total = sum(sim for _, _, sim in indexes)
        return total / max(len(A), len(B))
    return 0

# returns a mapping from "dimension down" to "matches at that level"
def lcs_multi_dimension(A, B, dimension):    
    dimension_matches = {i : [] for i in range(1, dimension + 1)}

    dimension_matches[1] = lcs_similarity(A, B, list_similiarity_function)

    for dimension_down in range(1, dimension):
        for path_a, path_b, _ in dimension_matches[dimension_down]:
            list_a = list_from_path(A, path_a)
            list_b = list_from_path(B, path_b)

            matches = lcs_similarity(list_a, list_b, list_similiarity_function)
            for idx_a, idx_b, sim in matches:
                dimension_matches[dimension_down + 1].append((path_a + idx_a, path_b + idx_b, sim))

    return dimension_matches

def get_matching_path(dim_matches, path_is_A, path):
    for path_a, path_b, sim in dim_matches[len(path)]:
        if path_is_A:
            if path_a == path:
                return path_b, sim
        else:
            if path_b == path:
                return path_a, sim
    return None, None


def inserted_paths(A, B, dim_matches):
    return inserted_paths_rec(A, B, dim_matches, False, [])

"""
Returns a tuple of (inserted rows, inserted columns):
inserted rows is a list of raw paths (also just lists)
the last index in an inserted column is not the row that was inserted but the column
"""
def inserted_paths_rec(A, B, dim_matches, first_list, base_path):
    if len(base_path) == max(dim_matches):
        return ([], [])

    # if this current thing was inserted
    lower_level_inserted_rows = []
    lower_level_inserted_cols = []
    add_curr_list = True
    indices = reversed(range(len(B))) if first_list else range(len(B)) # we go backwards if we are removing, so we don't have to shift
    for idx in indices:
        # if a path is matched, then things may have been inserted below it
        matching_path, _ = get_matching_path(dim_matches, first_list, base_path + [idx])
        if matching_path is not None:
            inserted_rows, inserted_cols = inserted_paths_rec(A[matching_path[-1]], B[idx], dim_matches, False, base_path + [idx])
            lower_level_inserted_rows.extend(inserted_rows)
            lower_level_inserted_cols.extend(inserted_cols)
            add_curr_list = False
        else:
            lower_level_inserted_rows.append(base_path + [idx])

    if add_curr_list:
        # we don't need to add anything below it, we can just add it as a whole
        return ([base_path], [])
    else:
        # now we try and see if these rows have a new column being created (happens at the bottom)
        two_deep_insertions = [x for x in lower_level_inserted_rows if len(x) == len(base_path) + 2]
        num_inserted_in_column = {path[-1] : 0 for path in two_deep_insertions} 
        for path in two_deep_insertions:
            num_inserted_in_column[path[-1]] += 1

        # if we also inserted a whole row, then we inserted all elements of that column a well
        one_deep_insertions = [x for x in lower_level_inserted_rows if len(x) == len(base_path) + 1]
        for path in one_deep_insertions:
            if len(path) < max(dim_matches):
                for col in range(len(B[path[-1]])):
                    if col not in num_inserted_in_column:
                        num_inserted_in_column[col] = 0
                    num_inserted_in_column[col] += 1
        
        for column in num_inserted_in_column:
            # find the number of rows that contain this column, as the lists are not rectangular
            column_length = sum(1 for row in B if column < len(row))

            if num_inserted_in_column[column] == column_length:
                lower_level_inserted_cols.append(base_path + ["_", column])
                # clear insertions from rows
                for path in two_deep_insertions:
                    if path[-1] == column:
                        lower_level_inserted_rows.remove(path)

        # and then we see if there are any columns we can unify
        to_delete = []
        for path in lower_level_inserted_cols:
            if len(path) >= len(base_path) + 2 and path[len(base_path) + 1] == "_":
                to_delete.append(path)

        if len(to_delete) == len(B):
            # we can unify 
            new_path = deepcopy(to_delete[0])
            new_path[len(base_path)] = "_"
            lower_level_inserted_cols.append(new_path)

            for path in to_delete:
                lower_level_inserted_cols.remove(path)

        return (lower_level_inserted_rows, lower_level_inserted_cols)


def removed_paths(A, B, dim_matches):
    # A deleted path is also a path that was added from the new list to the old list
    return inserted_paths_rec(B, A, dim_matches, True, [])

def changed_paths(A, B, dim_matches):
    changed = []
    for path in lowest_dim_paths(B, max(dim_matches), []):
        matching_path, sim = get_matching_path(dim_matches, False, path)
        if sim is not None and sim < 1:
            changed.append(path)

    return changed


def lowest_dim_paths(B, dim, base_path):
    if dim == 1:
        return [base_path + [idx] for idx in range(len(B))]
    
    paths = []
    for idx in range(len(B)):
        paths.extend(lowest_dim_paths(B[idx], dim - 1, base_path + [idx]))
    return paths





    

