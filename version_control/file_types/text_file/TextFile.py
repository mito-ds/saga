from copy import deepcopy
from version_control.file_types.file.File import File
from version_control.file_types.text_file.TextOpDeleteLine import TextOpDeleteLine
from version_control.file_types.text_file.TextOpInsertLine import TextOpInsertLine
from version_control.file_types.text_file.TextOpChangeLine import TextOpChangeLine


class TextFile(File):

    # A text file is a map from line number to text data
    def __init__(self, file_name, file_contents):
        File.__init__(self, file_name)
        self.file_contents = file_contents

    def get_lcs_indexes(self, new_file):
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
            if self.file_contents[i-1] == new_file.file_contents[j-1]: 
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


    def operations_from_range(self, new_file, old_start, old_end, new_start, new_end, num_deleted):
        print("A: {} - {}".format(old_start, old_end))
        print("B: {} - {}".format(new_start, new_end))
        A = self.file_contents[old_start: old_end]
        B = new_file.file_contents[new_start: new_end]
        print("A : {}".format(A))
        print("B : {}".format(B))

        patches = []
        for a_idx, _ in enumerate(A):
            line_number = new_start + a_idx - num_deleted
            if a_idx < len(B):
                patches.append(TextOpChangeLine(self.file_name, line_number, B[a_idx]))
            else:
                patches.append(TextOpDeleteLine(self.file_name, line_number))
                num_deleted += 1

        for b_idx, b in enumerate(B):
            if b_idx < len(A):
                continue
            else:
                line_number = new_start + b_idx - num_deleted
                patches.append(TextOpInsertLine(self.file_name, line_number, b))

        return patches, num_deleted

    def get_operations(self, new_file):
        if new_file.file_name != self.file_name:
            raise Exception("Can only get operations on the same files")

        lcs_indexes_old, lcs_indexes_new = self.get_lcs_indexes(new_file)
        print("Old : {}".format(lcs_indexes_old))
        print("New : {}".format(lcs_indexes_new))

        patches = []
        num_deleted = 0
        for i in range(len(lcs_indexes_old) - 1):
            new_patches, num_deleted = self.operations_from_range(
                new_file, 
                lcs_indexes_old[i] + 1, 
                lcs_indexes_old[i + 1], 
                lcs_indexes_new[i] + 1, 
                lcs_indexes_new[i + 1],
                num_deleted
            )
            patches += new_patches

        if len(lcs_indexes_old) == 0:
            new_patches, num_deleted = self.operations_from_range(
                new_file, 
                0, 
                len(self.file_contents), 
                0, 
                len(new_file.file_contents),
                0
            )
            patches += new_patches

        return patches

    def print_changes(self, new_file):
        if new_file.file_name != self.file_name:
            raise Exception("Can only print operations on the same files")

        lcs_indexes_old, lcs_indexes_new = self.get_lcs_indexes(new_file)

        old_idx = 0
        new_idx = 0
        print("File diff: {}".format(self.file_name))
        while old_idx < len(self.file_contents) or new_idx < len(new_file.file_contents):
            # first check if it's a change
            #if not (old_idx + 1 not in lcs_indexes_old and old_idx + 1 < len(self.file_contents)) and new_idx not in lcs_indexes_new and new_idx < len(new_file.file_contents):
            #    print(self.file_contents[old_idx] + " -> " + new_file.file_contents[new_idx])
            #    old_idx += 1
            #    new_idx += 1
            # first print all the deletes
            if old_idx not in lcs_indexes_old and old_idx < len(self.file_contents):
                print("- " + self.file_contents[old_idx])
                old_idx += 1
            # then print all inserts
            elif new_idx not in lcs_indexes_new and new_idx < len(new_file.file_contents):
                print("+ " + new_file.file_contents[new_idx])
                new_idx += 1
            else:
                # should march in unison
                assert new_file.file_contents[new_idx] == self.file_contents[old_idx]
                print(self.file_contents[old_idx])
                old_idx += 1
                new_idx += 1

    def change_line(self, line_number, line_contents):
        self.file_contents[line_number] = line_contents

    def insert_line(self, line_number, line_contents):
        self.file_contents.insert(line_number, line_contents)

    def delete_line(self, line_number):
        # line numbers are the numbers in the current file
        del self.file_contents[line_number]

    def to_string(self):
        return "TextFile\t{}\t{}".format(self.file_name, "%".join(self.file_contents))

    @staticmethod
    def from_string(file_string):
        file_string = file_string.split("\t")
        file_name = file_string[1]
        file_contents = file_string[2].split("%")
        return TextFile(file_name, file_contents)

    def to_file(self, file_path):
        assert file_path.endswith(self.file_name)
        f = open(file_path, "w+")
        f.write("\n".join(self.file_contents))
        f.close()

    @staticmethod
    def from_file(file_path):
        f = open(file_path, "r")
        file_contents = []
        for line in f.readlines():
            if line.endswith("\n"):
                file_contents.append(line[:len(line) - 1])
            else:
                file_contents.append(line)
        return TextFile(file_path, file_contents)