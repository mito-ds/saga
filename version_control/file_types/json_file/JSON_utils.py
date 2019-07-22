
PRIMITIVES = [int, float, str, bool, chr]


def json_equals(obj1, obj2):
    if type(obj1) != type(obj2):
        return False
    elif obj1 == obj2:
        return True
    elif type(obj1) in PRIMITIVES:
        return obj1 == obj2

    if isinstance(obj1, list):
        if len(obj1) != len(obj2):
            return False
        for i in range(len(obj1)):
            if not json_equals(obj1[i], obj2[i]):
                return False
        return True
    else:
        assert isinstance(obj1, dict)
        keys = set(obj1.keys()).union(set(obj2.keys()))
        for key in keys:
            if key not in obj1 or key not in obj2:
                return False
            if not json_equals(obj1[key], obj2[key]):
                return False
        return True

def get_lcs_indexes(list1, list2):
    # adapated from geeksforgeeks
    m = len(list1) 
    n = len(list2) 

    # L[i][j] is the length of the longest common subsequece up to indexes i, j
    L = [[None]*(n + 1) for i in range(m + 1)] 
    for i in range(m + 1): 
        for j in range(n + 1): 
            if i == 0 or j == 0 : 
                L[i][j] = 0
            elif json_equals(list1[i - 1], list2[j - 1]): 
                L[i][j] = L[i - 1][j - 1]+1
            else: 
                L[i][j] = max(L[i - 1][j], L[i][j - 1]) 

    if L[m][n] == len(list1) and L[m][n] == len(list2):
        # the files are the same, in this case
        return ([i for i in range(L[m][n])], [i for i in range(L[m][n])])

    # Create an array to store indexes of common subsequence
    lcs_indexes_old = [0] * (L[m][n]) 
    lcs_indexes_new = [0] * (L[m][n])
    index = L[m][n] - 1

    # Start from the right-most-bottom-most corner and 
    # one by one store characters in lcs[] 
    i = m 
    j = n 
    while i > 0 and j > 0: 

        # If current character in X[] and Y are same, then 
        # current character is part of LCS 
        if json_equals(list1[i-1], list2[j-1]): 
            lcs_indexes_old[index] = i-1 
            lcs_indexes_new[index] = j-1 
            i-=1
            j-=1
            index-=1

        # If not same, then find the larger of two and 
        # go in the direction of larger value 
        elif L[i-1][j] > L[i][j-1]: 
            i-=1
        else: 
            j-=1

    return (lcs_indexes_old, lcs_indexes_new)