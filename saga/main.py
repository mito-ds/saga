#!/usr/bin/env python3
import argparse
import os
import pickle
from saga.Repository import Repository

def main():
    parser = argparse.ArgumentParser(description='Do version control on some files')
    parser.add_argument('action', type=str, help='')
    parser.add_argument('file', type=str, help='', nargs='?')
    parser.add_argument('message', type=str, help='', nargs='?')

    args = parser.parse_args()
    cwd = os.getcwd()
    # First, we find out if this folder is the part of an existing .vcs project
    vcs_base_path = get_vcs_base_path(cwd)

    # Handle the case where the project has not been started; the only option is to create it
    repository = None

    if args.action == "init":
        if vcs_base_path is None:
            repository = Repository.init(cwd)
            vcs_base_path = cwd
            print("Saga project created at {}".format(vcs_base_path))
        else:
            print("Error: saga project already exists at {}".format(vcs_base_path))
            return
    else:
        if vcs_base_path is None:
            print("Error: must create saga project before using it")
            return
        repository = Repository.read(vcs_base_path) 

    if args.action == "diff":
        repository.get_diff()
    elif args.action == "add":
        repository.add(args.file)
        print(repository.index)
    elif args.action == "commit":
        repository.commit(args.message)
    elif args.action == "branch":
        print("HEAD: {}".format(repository.head))
        print(repository.branches)
    elif args.action == "status":
        repository.status() 
    elif args.action == "newbranch":
        repository.create_branch(args.message)
    elif args.action == "switchbranch":
        repository.switch_to_branch(args.message)
    elif args.action == "init":
        pass # we handle this above
    elif args.action == "index":
        print(repository.index)
        print(repository.file_ids)
    elif args.action == "merge":
        repository.merge(args.message)
    else:
        print("Error: usage {init | add | commit | diff}")

    repository.write()

def get_vcs_base_path(cwd):
    path = cwd
    while path != "/":
        # check if there is a
        if os.path.isdir(path + "/.saga"):
            return path
        path = os.path.dirname(path)
    return None

main()