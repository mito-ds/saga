"""
Helper functions for computing longest-common-subsequences:
with a similarity function and without.
"""



def lcs(A, B):
    def equal(a, b):
        if a == b:
            return 1
        return 0

    return lcs_similarity(A, B, equal)

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
    lcs_indexes_old = []
    lcs_indexes_new = []

    # Start from the right-most-bottom-most corner and 
    # one by one store characters in lcs[] 
    i = m 
    j = n 
    while i > 0 and j > 0:

        # If current character in X[] and Y are same, then 
        # current character is part of LCS 
        if similarity_function(A[i - 1], B[j - 1]) + L[i - 1][j - 1] > max(L[i - 1][j], L[i][j - 1]): 
            lcs_indexes_old.append(i - 1) 
            lcs_indexes_new.append(j - 1)
            i-=1
            j-=1

        # If not same, then find the larger of two and 
        # go in the direction of larger value 
        elif L[i-1][j] > L[i][j-1]:
            i-=1
        else: 
            j-=1

    lcs_indexes_old.reverse()
    lcs_indexes_new.reverse()
    return (lcs_indexes_old, lcs_indexes_new)


def arr_equals(A, B):
    if len(A) != len(B):
        return False
    if type(A) in (int, float, bool, str) and type(B) in (int, float, bool, str):
        return A == B
    for a, b in zip(A, B):
        if not arr_equals(a, b):
            return False
    return True

# returns a mapping from "dimension down" to "matches at that level"
def lcs_multi_dim(A, B, dim, similarity_function):

    if dim == 1:
        return lcs_similarity(A, B, similarity_function)
    return None

    





