import os
from version_control.file_types.file.File import File
from version_control.file_types.csv_file.CSVFileOpRemoveRow import CSVFileOpRemoveRow
from version_control.file_types.csv_file.CSVFileOpInsertRow import CSVFileOpInsertRow
from version_control.file_types.csv_file.CSVFileOpRemoveColumn import CSVFileOpRemoveColumn
from version_control.file_types.csv_file.CSVFileOpInsertColumn import CSVFileOpInsertColumn
from version_control.file_types.csv_file.CSVFileOpChangeValue import CSVFileOpChangeValue
from version_control.lcs import lcs_multi_dimension

class CSVFile(File):

    def __init__(self, file_name, file_contents):
        File.__init__(self, file_name)
        self.file_contents = file_contents


    def insert_row(self, index, value):
        if not isinstance(value, list):
            raise Exception("value is not a list")
        
        self.file_contents.insert(index, value)
            
    def insert_column(self, index, value):
        if not isinstance(value, list):
            raise Exception("value is not a list")
    
        for i, row in enumerate(self.file_contents):
            row.insert(index, value[i])

    def remove_row(self, index):
        self.file_contents.pop(index)

    def remove_column(self, index):
        for row in self.file_contents:
            row.pop(index)

    def change_value(self, row, column, value):
        self.file_contents[row][column] = value

    def get_operations(self, new_file):
        dim_matches = lcs_multi_dimension(self.file_contents, new_file.file_contents, 2)

        delete_patches_row = []
        for line_number in range(len(self.file_contents)):
            matched = False
            for old, _, _ in dim_matches[1]:
                if old[0] == line_number:
                    matched = True

            if not matched:
                relative_line_num = line_number - len(delete_patches_row) # get the relative number, accounting for lines deleted before
                delete_patches_row.append(CSVFileOpRemoveRow(self.file_name, relative_line_num))

        insert_patches_row = []
        for line_number in range(len(new_file.file_contents)):
            matched = False
            for _, new, sim in dim_matches[1]:
                if new[0] == line_number:
                    matched = True
                    break

            if not matched:
                insert_patches_row.append(CSVFileOpInsertRow(self.file_name, line_number, new_file.file_contents[line_number]))
                

        # Now we search for where columns were deleted
        delete_patches_col = []
        for line_number in range(len(self.file_contents[0])):
            matched = False
            for path, _, _ in dim_matches[2]:
                if path[1] == line_number:
                    matched = True
                    break

            if not matched:
                relative_line_num = line_number - len(delete_patches_col) # get the relative number, accounting for lines deleted before
                delete_patches_col.append(CSVFileOpRemoveColumn(self.file_name, relative_line_num))

        insert_patches_col = []
        added_columns = set()
        for line_number in range(len(new_file.file_contents[0])):
            matched = False
            for _, path, _ in dim_matches[2]:
                if path[1] == line_number:
                    matched = True

            if not matched:
                column = []
                for row in new_file.file_contents:
                    column.append(row[line_number])
                added_columns.add(line_number)
                insert_patches_col.append(CSVFileOpInsertColumn(self.file_name, line_number, column))

        change_patches = []
        # or if, a row that has been matched but has less than 100% similarity
        # and an element in a column is not matched and also is not in a column
        # that has been inserted
        for _, row_new, sim in dim_matches[1]:
            row_new = row_new[0]
            if sim < 1:
                for idx, ele in enumerate(new_file.file_contents[row_new]):
                    if idx not in added_columns:
                        # if it was not matched with similarity 1, then it was changed
                        changed = True
                        for _, path, sim in dim_matches[2]:
                            if path[0] == row_new and idx == path[1] and sim == 1:
                                changed = False

                        if changed:
                            change_patches.append(CSVFileOpChangeValue(self.file_name, row_new, idx, ele))


        return delete_patches_row + insert_patches_row + delete_patches_col + insert_patches_col + change_patches

    def to_string(self):
        pass

    @staticmethod
    def from_string(file_string):
        pass

    def to_file(self, file_path):
        pass

    @staticmethod
    def from_file(file_path):
        pass

    def print_changes(self, new_file):
        ops = self.get_operations(new_file)
        print(ops)

            
