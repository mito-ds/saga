from copy import deepcopy
from colorama import Fore, Style
from version_control.file_types.file.File import File
from version_control.file_types.text_file.TextOpDeleteLine import TextOpDeleteLine
from version_control.file_types.text_file.TextOpInsertLine import TextOpInsertLine


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

    def get_operations(self, new_file):
        if new_file.file_name != self.file_name:
            raise Exception("Can only get operations on the same files")

        lcs_indexes_old, lcs_indexes_new = self.get_lcs_indexes(new_file)

        delete_patches = []
        for line_number in range(len(self.file_contents)):
            if line_number not in lcs_indexes_old:
                relative_line_num = line_number - len(delete_patches) # get the relative number, accounting for lines deleted before
                delete_patches.append(TextOpDeleteLine(self.file_name, relative_line_num))

        insert_patches = []
        for line_number in range(len(new_file.file_contents)):
            if line_number not in lcs_indexes_new:
                insert_patches.append(TextOpInsertLine(self.file_name, line_number, new_file.file_contents[line_number]))

        return delete_patches + insert_patches

    def print_changes(self, new_file):
        if new_file.file_name != self.file_name:
            raise Exception("Can only print operations on the same files")

        lcs_indexes_old, lcs_indexes_new = self.get_lcs_indexes(new_file)

        old_idx = 0
        new_idx = 0
        print("File diff: {}".format(self.file_name))
        while old_idx < len(self.file_contents) and new_idx < len(new_file.file_contents):
            # first print all the deletes
            if old_idx not in lcs_indexes_old:
                print(Fore.RED + "- " + self.file_contents[old_idx])
                old_idx += 1
            # then print all inserts
            elif new_idx not in lcs_indexes_new:
                print(Fore.GREEN + "+ " + new_file.file_contents[new_idx])
                new_idx += 1
            else:
                # should march in unison
                assert new_file.file_contents[new_idx] == self.file_contents[old_idx]
                print(Fore.BLACK + self.file_contents[old_idx])
                old_idx += 1
                new_idx += 1


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