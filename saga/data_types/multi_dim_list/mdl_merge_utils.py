from saga.data_types.multi_dim_list.lcs import lcs

# diff3 merge
def diff3(A, O, B):
    matchings_A = lcs(A, O)
    matchings_B = lcs(B, O)

    # increment all the indexes by one
    matchings_A = [([a + 1], [o + 1], sim) for ([a], [o], sim) in matchings_A]
    matchings_B = [([b + 1], [o + 1], sim) for ([b], [o], sim) in matchings_B]

    chunks = get_chunks(A, O, B, matchings_A, matchings_B)

    string_output_chunks = chunks_to_output(A, O, B, matchings_A, matchings_B, chunks)

    return create_merged_file(string_output_chunks)

def get_chunks(A, O, B, matchings_A, matchings_B):
    chunks = []
    idx_A, idx_O, idx_B = 0, 0, 0
    max_idx_A, max_idx_O, max_idx_B = len(A), len(O), len(B)

    i = 1
    while not (i + idx_A > max_idx_A or i + idx_O > max_idx_O or i + idx_B > max_idx_B):
        if not is_matching(matchings_A, idx_A + i, idx_O + i) or not is_matching(matchings_B, idx_B + i, idx_O + i):
            # unstable 
            if i == 1:
                # find index end of unstable chunk
                for j in range(idx_O + 1, max_idx_O + 1):
                    last_indexes = is_stable_index(matchings_A, matchings_B, j)
                    if last_indexes:
                        # found last index of unstable chunk
                        (end_A, end_O, end_B) = last_indexes
                        unstable_chunk = ((idx_A + 1, end_A - 1), (idx_O + 1, end_O - 1), (idx_B + 1, end_B - 1))
                        chunks.append(unstable_chunk)
                        idx_A, idx_O, idx_B = end_A - 1, end_O - 1, end_B - 1
                        i = 1
                        break

            # stable
            else:
                stable_chunk = ((idx_A + 1, idx_A + i - 1), (idx_O + 1, idx_O + i - 1), (idx_B + 1, idx_B + i - 1))
                chunks.append(stable_chunk)
                idx_A, idx_O, idx_B = idx_A + i - 1, idx_O + i - 1, idx_B + i - 1
                i = 1
        else:
            i += 1
    else:
        last_chunk = ((idx_A + 1, max_idx_A), (idx_O + 1, max_idx_O), (idx_B + 1, max_idx_B))
        chunks.append(last_chunk)
        return chunks

def create_merged_file(chunks):
    merged_file = []
    conflicting_chunks = []
    for i, chunk in enumerate(chunks):
        (s_A, s_O, s_B) = chunk
        if not s_A == s_B:
            conflicting_chunks.append((i, chunk))
        else:
            merged_file.extend(s_A)

    if not any(conflicting_chunks):
        return merged_file
    return None

def chunks_to_output(A, O, B, matchings_A, matchings_B, chunks):
    calculated_ouput = []

    for chunk in chunks:

        ((s_A, e_A), (s_O, e_O), (s_B, e_B)) = chunk

        a_changed = chunk_changed(matchings_A, s_A, e_A, s_O, e_O)
        b_changed = chunk_changed(matchings_B, s_B, e_B, s_O, e_O)

        if a_changed and not b_changed:
            calculated_ouput.append(chunk_changed_in_A(chunk, A))
        elif b_changed and not a_changed:
            calculated_ouput.append(chunk_changed_in_B(chunk, B))
        else:
            calculated_ouput.append(chunk_conflicting_or_stable(chunk, A, B, O))

    return calculated_ouput

def chunk_changed_in_A(chunk, A):
    #output A[H], A[H], A[H]
    ((s_A, e_A), _, _) = chunk
    string = A[s_A - 1 : e_A]
    return (string, string, string)

def chunk_changed_in_B(chunk, B):
    #output B[H], B[H], B[H]
    (_, _, (s_B, e_B)) = chunk
    string = B[s_B  -1 : e_B]
    return (string, string, string)

def chunk_conflicting_or_stable(chunk, A, B, O):
    #output A[H], O[H], B[H]
    ((s_A, e_A), (s_O, e_O), (s_B, e_B)) = chunk
    return (A[s_A - 1: e_A], O[s_O - 1: e_O ], B[s_B - 1: e_B ])

def chunk_changed(matchings, s, e, s_O, e_O):

    for i in range (s, e + 1):
            if not matched(matchings, i):
                return True

    for i in range (s_O, e_O + 1):
            if not matched_O(matchings, i):
                return True

    return False

# returns true if a matching exists with this index of A or B
def matched(matchings, idx):
    for match in matchings:
        ([i], _, _) = match
        if (i == idx):
            return True
    return False

# returns true if a matching exists with this index of A or B
def matched_O(matchings, idx):
    for match in matchings:
        (_, [i], _) = match
        if (i == idx):
            return True
    return False

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
