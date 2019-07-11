from version_control.file_types.file.File import File

class TextFile(File):

    # A text file is a map from line number to text data
    # it's an array of strings, tbh; just bump everything up when you need to
    def __init__(self, file_name, file_contents):
        File.__init__(self, file_name)
        self.file_contents = file_contents

    def get_operations(self, new_file):
        # TODO: implement longest common subsequence operations...
        # it's probably the best heuristic here?
        if new_file.file_name != self.file_name:
            raise Exception("Can only get operations on the same files")

        # adapated from geeksforgeeks
        m = len(self.file_contents) 
        n = len(new_file.file_contents) 

        # L[i][j] is the length of the longest common subsequece up to indexes i, j
        L = [[None]*(n + 1) for i in range(m + 1)] 
        for i in range(m + 1): 
            for j in range(n + 1): 
                if i == 0 or j == 0 : 
                    L[i][j] = 0
                elif self.file_contents[i-1] == new_file.file_contents[j-1]: 
                    L[i][j] = L[i-1][j-1]+1
                else: 
                    L[i][j] = max(L[i-1][j], L[i][j-1]) 

        if L[m][n] == len(self.file_contents) and L[m][n] == len(new_file.file_contents):
            # the files are the same, in this case
            return []
    
        # Create an array to store indexes of common subsequence
        lcs_indexes_i = [0] * (L[m][n]) 
        lcs_indexes_j = [0] * (L[m][n])
        index = L[m][n] - 1
    
        # Start from the right-most-bottom-most corner and 
        # one by one store characters in lcs[] 
        i = m 
        j = n 
        while i > 0 and j > 0: 
    
            # If current character in X[] and Y are same, then 
            # current character is part of LCS 
            if self.file_contents[i-1] == new_file.file_contents[j-1]: 
                lcs_indexes_i[index] = i-1 
                lcs_indexes_j[index] = j-1 
                i-=1
                j-=1
                index-=1
    
            # If not same, then find the larger of two and 
            # go in the direction of larger value 
            elif L[i-1][j] > L[i][j-1]: 
                i-=1
            else: 
                j-=1
        


        print(lcs_indexes_i)
        print(lcs_indexes_j)



    def change_line(self, line_number, line_contents):
        if line_number >= len(self.file_contents):
            raise Exception("cannot change line that is greater than contents")
        self.file_contents[line_number] = line_contents

    def insert_line(self, line_number, line_contents):
        self.file_contents.insert(line_number, line_contents)

    def delete_line(self, line_number):
        self.file_contents.pop(line_number)