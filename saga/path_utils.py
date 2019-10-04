import os
import shutil
import glob
import filecmp

def copy_dir_to_dir(src, dst, exclude=None):
    """
    src is a relative path. It must be a folder that exists.
    dst is an absolute path. It will be created if it does not exist.

    If a path = src/file_name, then this will be copied to dst/file_name
    """
    if exclude is None:
        exclude = []
    if src[-1] == "/":
        src = src[:-1]

    if not os.path.exists(dst):
            os.makedirs(dst)

    # otherwise, we recursively expore the directory and copy it over
    for root, dirs, files in os.walk(src):
        dirs[:] = [d for d in dirs if d not in exclude]
        relative_root = root[len(src) + 1:]

        # first we copy the directories
        for directory in dirs:
            # if the directory doesn't exist, we make it
            path = os.path.join(dst, relative_root, directory)
            if not os.path.isdir(path):
                os.mkdir(path)

        # and then the files
        for file_name in files:
            path = os.path.join(dst, relative_root, file_name)
            shutil.copyfile(os.path.join(root, file_name), path)

def copy_file_to_dir(src, dst):
    """
    src is a relative path of a file. 
    dst is an absolute path of a folder. 

    src will eixst at join(dst, src)
    """
    dirname = os.path.join(dst, os.path.dirname(src))
    print(dirname)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)

    shutil.copyfile(src, os.path.join(dst, src))

def relative_paths_in_dir(directory, ignore=None):
    """
    Returns a list of paths in the directory, excluding paths that begin with ignore
    """
    if ignore is None:
        ignore = []

    # we make sure that the path does not start with a slash
    if directory[-1] == "/":
        paths = [path[len(directory):] for path in glob.glob(directory + '/**', recursive=True) if path[len(directory):] != ""]
    else:
        paths = [path[len(directory) + 1:] for path in glob.glob(directory + '/**', recursive=True) if path[len(directory) + 1:] != ""]
    def include_path(path):
        for ignore_path in ignore:
            if path.startswith(ignore_path):
                return False
        if path == directory:
            return False
        return True
    return {path for path in paths if include_path(path)}

def changed_files(dir1, dir2):
        previous_state = relative_paths_in_dir(dir1)
        current_state = relative_paths_in_dir(dir2)

        removed_paths, changed_paths, inserted_paths  = set(), set(), set()
        for path in previous_state:
            if path not in current_state:
                removed_paths.add(path)
            else:
                path1 = os.path.join(dir1, path)
                path2 = os.path.join(dir2, path)
                if os.path.isfile(path1) and os.path.isfile(path2) and not filecmp.cmp(path1, path2):
                    changed_paths.add(path)
                elif (os.path.isfile(path1) and not os.path.isfile(path2)) or \
                    (not os.path.isfile(path1) and os.path.isfile(path2)):
                    changed_paths.add(path)
        for path in current_state:
            if path not in previous_state:
                inserted_paths.add(path)

        return removed_paths, changed_paths, inserted_paths