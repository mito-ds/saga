from pathlib import Path
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
    path = Path(folder_path)
    origin = parse_file("id", "file", path / f"origin.{ending}")
    a = parse_file("id", "file", path / f"a.{ending}")
    b = parse_file("id", "file", path / f"b.{ending}")
    merge = parse_file("id", "file", path / f"merge.{ending}")
    calculated_merge = origin.merge(a, b)

    return merge.file_contents == calculated_merge.file_contents



