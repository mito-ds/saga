import difflib



def lcs(array1, array2):
    # adapated from geeksforgeeks
    m = len(array1) 
    n = len(array2) 

    # L[i][j] is the length of the longest common subsequece up to indexes i, j
    L = [[None]*(n + 1) for i in range(m + 1)] 
    for i in range(m + 1): 
        for j in range(n + 1): 
            if i == 0 or j == 0 : 
                L[i][j] = 0
            elif array1[i-1] == array2[j-1]: 
                L[i][j] = L[i-1][j-1]+1
            else: 
                L[i][j] = max(L[i-1][j], L[i][j-1]) 

    if L[m][n] == len(array1) and L[m][n] == len(array2):
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
        if array1[i-1] == array2[j-1]: 
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



def string_distance(a, b):
    return difflib.SequenceMatcher(None, a, b).ratio()


def lcs_close(A, B):
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
                    string_distance(A[i - 1], B[j - 1]) + L[i - 1][j - 1],
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
        if string_distance(A[i - 1], B[j - 1]) + L[i - 1][j - 1] > max(L[i - 1][j], L[i][j - 1]): 
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