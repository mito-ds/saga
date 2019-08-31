"""
A set of functions for computing longest-common subsequences between lists.
"""


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
    if len(A) == 0 and len(B) == 0:
        return 1

    indexes = lcs(A, B)
    if any(indexes):
        return len(indexes) / max(len(A), len(B))
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


def path_matched(dim_matches, first_list, path):
    for path_a, path_b, sim in dim_matches[len(path)]:
        if first_list:
            if path_a == path:
                return True
        else:
            if path_b == path:
                return True
    return False


