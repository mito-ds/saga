"""
Functions for computing longest-common subsequences between lists
"""
from copy import deepcopy

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
    
    matches.reverse()

    return matches

# Standard LCS: the similarity function is just exact equality
def lcs(A, B):
    def equal(a, b):
        if a == b:
            return 1
        return 0

    return lcs_similarity(A, B, equal)


def list_from_path(matrix, path):
    curr = matrix
    for step in path:
        curr = curr[step]
    return curr

def same_paths(dict_a, dict_b):
    return {k for k in dict_a if k in dict_b and dict_a[k] == dict_b[k]}

def similarity_function(A, B):
    if type(A) != type(B):
        return 0
    elif A is None:
        return 1
    elif type(A) in (int, float, bool):
        return 1 if A == B else 0
    elif type(A) == str:
        if len(A) == 0 and len(B) == 0:
            return 1
        indexes = lcs(A, B)
        if any(indexes):
            return len(indexes) / max(len(A), len(B))
        return 0
    elif type(A) == list:
        if len(A) == 0 and len(B) == 0:
            return 1
            
        A = [a for a in A if a is not None]
        B = [b for b in B if b is not None]

        indexes = lcs_similarity(A, B, similarity_function)
        if any(indexes):
            total = sum(sim for _, _, sim in indexes)
            return total / max(len(A), len(B))
        return 0
    elif type(A) == dict:
        # we just do the number of unchanged keys divided by the max number of keys
        unchanged = same_paths(A, B)
        if any(unchanged):
            return len(unchanged) / max(len(A), len(B))
        return 0

    else:
        print("Unknown type {}".format(type(A)))
        return 0

def lcs_with_sim(A, B):
    return lcs_similarity(A, B, similarity_function)

# returns a mapping from "dimension down" to "matches at that level"
def lcs_multi_dimension(A, B):    
    dimension_matches = dict()
    dimension_matches[1] = lcs_similarity(A, B, similarity_function)

    dimension = 1
    matches = dimension_matches[1]
    while any(matches):
        dimension += 1
        dimension_matches[dimension] = []
        for path_a, path_b, _ in dimension_matches[dimension - 1]:
            list_a = list_from_path(A, path_a)
            list_b = list_from_path(B, path_b)
            if type(list_a) != list or type(list_b) != list:
                matches = []
                break

            matches = lcs_similarity(list_a, list_b, similarity_function)
            for idx_a, idx_b, sim in matches:
                dimension_matches[dimension].append((path_a + idx_a, path_b + idx_b, sim))

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



    

