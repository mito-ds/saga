#!/usr/bin/env python3
import argparse
import os
from version_control.Patch import Patch
from version_control.Branch import Branch
from version_control.file_types.file.FileOpAdd import FileOpAdd
from version_control.file_types.file.FileOpRemove import FileOpRemove
from version_control.file_types.text_file.TextFile import TextFile
from version_control.file_types.binary_file.BinaryFile import BinaryFile

def main():
    parser = argparse.ArgumentParser(description='Do version control on some files')
    parser.add_argument('action', type=str, help='')
    parser.add_argument('file', type=str, help='', nargs='?')

    args = parser.parse_args()
    cwd = os.getcwd()
    # First, we find out if this folder is the part of an existing .vcs project
    vcs_path = get_vcs_path(cwd)

    # Handle the case where the project has not been started; the only option is to create it
    if vcs_path is None:
        if args.action == "init":
            init_vcs_folder(cwd)
        else:
            print("Error: must create a vcs project using init before running other commands")
        return

    curr_state = get_curr_state(vcs_path)

    if args.action == "init":
        print("Error: vcs project already exists at {}".format(vcs_path))
    elif args.action == "commit":
        commit(vcs_path)
    elif args.file == None:
        print("Error: must specify a file")
    elif args.action == "add":
        add_file(cwd, args.file, curr_state)
    elif args.action == "diff":
        diff(vcs_path, args.file)
    else:
        print("Error: usage {init | add | commit | diff}")

def get_curr_state(vcs_path, include_working_commit=True):
    branch = Branch()

    for patch_file_name in os.listdir(vcs_path + "/branch"):
        f = open(vcs_path + "/branch/" + patch_file_name, "r")
        patch_file_text = f.read().strip()
        f.close()
        patch = Patch.from_string(patch_file_text)
        branch.add_patch(patch)
        
    if include_working_commit:
        f = open(vcs_path + "/curr_commit", "r")
        patch_file_text = f.read().strip()
        f.close()
        if patch_file_text == "":
            return branch.curr_state()
        patch = Patch.from_string(patch_file_text)
        branch.add_patch(patch)

    return branch.curr_state()

def get_vcs_path(cwd):
    path = cwd
    while path != "/":
        # check if there is a
        if os.path.isdir(path + "/.vcs"):
            return path + "/.vcs"
        path = os.path.dirname(path)
    return None

def init_vcs_folder(cwd):
    os.mkdir(cwd + "/.vcs")
    os.mkdir(cwd + "/.vcs/branch")
    f = open(cwd + "/.vcs/curr_commit", "w+")
    f.close()
    return cwd + "/.vcs"

def add_file(cwd, file_name, curr_state):
    # if the file existed before
    if file_name in curr_state:
        if not os.path.exists(file_name):
            # we are either deleting it
            add_op_to_curr_commit(FileOpRemove(file_name))
        else:
            # or we are changing it
            prev_file = curr_state.files[file_name]
            file_class = type(prev_file)
            new_file = file_class.from_file(file_name)
            change_operations = prev_file.get_operations(new_file)

            # write them to current commit
            for operation in change_operations:
                add_op_to_curr_commit(operation)
    else:
        # otherwise, it didn't exist before, so we are adding it
        if file_name.endswith(".txt"):
            file_obj = TextFile.from_file(file_name)
        else:
            file_obj = BinaryFile.from_file(file_name)
        add_op_to_curr_commit(FileOpAdd(file_name, file_obj))

def commit(vcs_path):
    # check that the current commit isn't empty:
    curr_commit = open(vcs_path + "/curr_commit", "r+")
    text = curr_commit.read()
    curr_commit.close()
    if text == "":
        print("Error: nothing to commit")
        return
    # this is a new file
    patch_file_name = "0"
    for patch_file_name in os.listdir(vcs_path + "/branch"):
        pass
    last = int(patch_file_name)
    new = last + 1
    # commit the current commit
    os.rename(vcs_path + "/curr_commit", vcs_path + "/branch/" + str(new))
    # make a new current commit
    f = open(vcs_path + "/curr_commit", "w+")
    f.close()

def diff(vcs_path, file_name):
    # if the file didn't exist
    curr_state = get_curr_state(vcs_path, include_working_commit=False)
    if file_name not in curr_state:
        if not os.path.exists(file_name):
            print("Error: no diff as file does not/didn't exist")
        else:
            if file_name.endswith(".txt"):
                file_obj = TextFile.from_file(file_name)
            else:
                file_obj = BinaryFile.from_file(file_name)
            print("File diff: {}".format(file_obj.file_name))
            print("+" + file_obj.file_contents)
    else:
        if not os.path.exists(file_name):
            file_obj = curr_state.files[file_name]
            print("File diff: {}".format(file_name))
            print("Deleted file")
        else:
            if file_name.endswith(".txt"):
                file_obj = TextFile.from_file(file_name)
            else:
                file_obj = BinaryFile.from_file(file_name)
            curr_state.files[file_name].print_changes(file_obj)

def add_op_to_curr_commit(operation):
    operation_string = operation.to_string()
    f = open(os.getcwd() + "/.vcs/curr_commit", "a+")
    f.write(operation_string + "\n")
    f.close()

main()