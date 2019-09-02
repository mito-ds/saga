from version_control.file_types.text_file import TextFile
from version_control.file_types.text_file.TextOpRemoveLine import TextOpRemoveLine
from version_control.file_types.text_file.TextOpInsertLine import TextOpInsertLine
from copy import deepcopy

# diff3 merge Text File
def diff3_merge_Text_File(A, O, B):
    #todo add a test to make sure it is a text file
    merge_conflicts = []
    nonconflicting_changes = []

    changes_A = O.get_operations(A)
    changes_B = O.get_operations(B)

    # find all merge conflicts and changes from O to A that do not conflict with changes O to B
    merge_conflicts, nonconflicting_changes = categorize_changes(changes_A, changes_B)

    # add changes from O to B that do not conflict
    for change_B in changes_B:
        if change_B not in merge_conflicts and change_B not in nonconflicting_changes:
            nonconflicting_changes.append(change_B)

    if len(merge_conflicts) > 0:
        return False
    else:
        return True


def categorize_changes(changes_X, changes_Y):
    merge_conflicts, nonconflicting_changes = [], []
    for change_X in changes_X:
        file_name_X = change_X.file_name
        line_number_X = change_X.line_number
        line_contents_X = ""
        change_type_X = TextOpRemoveLine
        conflict = False

        if isinstance(change_X, TextOpInsertLine):
            change_type_X = TextOpInsertLine
            line_contents_X = change_X.line_contents

        for change_Y in changes_Y:
            file_name_Y = change_Y.file_name
            line_number_Y = change_Y.line_number
            change_type_Y = TextOpRemoveLine
            line_contents_Y = ""

            if isinstance(change_Y, TextOpInsertLine):
                change_type_Y = TextOpInsertLine
                line_contents_Y = change_Y.line_contents

            if file_name_X == file_name_Y and line_number_X == line_number_Y:
                # different operations
                if not isinstance(change_Y, change_type_X):
                    conflict = True
                    merge_conflicts.append((change_X, change_Y))
                    break
                # same operation with different content
                elif not line_contents_X == line_contents_Y:
                    conflict = True
                    merge_conflicts.append((change_X, change_Y))
                    break

        if not conflict:
            nonconflicting_changes.append(change_X)

    return merge_conflicts, nonconflicting_changes
