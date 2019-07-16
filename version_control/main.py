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
    parser.add_argument('file', type=str, help='')
    args = parser.parse_args()
    cwd = os.getcwd()


    if args.action == "init":
        if os.path.isdir(cwd + "/.vcs"):
            print("Project already initialized")
        else:
            os.mkdir(cwd + "/.vcs")
            os.mkdir(cwd + "/.vcs/branch")
            f = open(cwd + "/.vcs/curr_commit", "w+")
            f.close()
    elif args.action == "add":
        curr_branch = get_current_branch()
        curr_state = curr_branch.curr_state()
        # if the file existed before
        if args.file in curr_state.files:
            # we are either deleting it
            if not os.path.exists(args.file):
                f = open(cwd + "/.vcs/curr_commit", "a+")
                f.write(FileOpRemove(args.file).to_string())
                f.close()
            # or we are changing it
            prev_file = curr_state.files[args.file]
            file_class = type(prev_file)
            new_file = file_class.from_file(args.file)
            change_operations = prev_file.get_operations(new_file)
            
            # write them to current commit
            for operation in change_operations:
                add_op_to_curr_commit(operation)
        else:
            if args.file.endswith(".txt"):
                file_obj = TextFile.from_file(args.file)
            else:
                file_obj = BinaryFile.from_file(args.file)
            add_op_to_curr_commit(FileOpAdd(args.file, file_obj))
    elif args.action == "commit":
        # this is a new file
        patch_file_name = "0"
        for patch_file_name in os.listdir(cwd + "/.vcs/branch"):
            pass
        last = int(patch_file_name)
        new = last + 1
        # commit the current commit
        os.rename(cwd + "/.vcs/curr_commit", cwd + "/.vcs/branch/" + str(new))
        # make a new current commit
        f = open(cwd + "/.vcs/curr_commit", "w+")
        f.close()
    else:
        print("Error: usage \{init | add | commit\}")
    



def get_current_branch():
    cwd = os.getcwd()
    branch = Branch()

    for patch_file_name in os.listdir(cwd + "/.vcs/branch"):
        f = open(cwd + "/.vcs/branch/" + patch_file_name, "r")
        patch_file_text = f.read().strip()
        f.close()
        patch = Patch.from_string(patch_file_text)
        branch.add_patch(patch)

    f = open(cwd + "/.vcs/curr_commit", "r")
    patch_file_text = f.read().strip()
    f.close()
    patch = Patch.from_string(patch_file_text)
    branch.add_patch(patch)

    return branch

def add_op_to_curr_commit(operation):
    operation_string = operation.to_string()
    f = open(os.getcwd() + "/.vcs/curr_commit", "a+")
    f.write(operation_string + "\n")
    f.close()

main()