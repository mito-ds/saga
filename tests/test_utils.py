import os
from saga.file_types.file_utils import parse_file


def do_test_merge(folder_path, ending):
    """
    folder_path should be a path to a folder with:
        - an original version of a file named `origin`
        - two modified versions, `a` and `b`
        - a merged version of these changes in the file `merge`

    This returns true iff a and b merged with the original as base
    results in the merged file!
    """ 
    origin = parse_file("id", "file", os.path.join(folder_path, "origin" + ending))
    a = parse_file("id", "file", os.path.join(folder_path, "a" + ending))
    b = parse_file("id", "file", os.path.join(folder_path, "b" + ending))
    merge = parse_file("id", "file", os.path.join(folder_path, "merge" + ending))
    print(origin.file_contents.mixed_data_type)
    print(a.file_contents.mixed_data_type)
    print(b.file_contents.mixed_data_type)
    print(merge.file_contents.mixed_data_type)
    calculated_merge = origin.merge(a, b)
    print(calculated_merge.file_contents.mixed_data_type)

    return merge.file_contents == calculated_merge.file_contents



