#!/usr/bin/env python3
import argparse
import os
from saga.Repository import Repository

def main():
    # create the top-level saga parser
    parser = argparse.ArgumentParser(prog='saga')
    subparsers = parser.add_subparsers(help='sub-command help')
    
    # create the parser for the "init" command
    parser_init = subparsers.add_parser('init', help='creates a new saga project in the current directory')
    parser_init.set_defaults(func=init)

    # create the parser for the "add" command
    parser_add = subparsers.add_parser('add', help='adds a path to the current index')
    parser_add.add_argument('path', type=str, help='the path to add to the index')
    parser_add.set_defaults(func=add)

    # create the parser for the "commit" command
    parser_commit = subparsers.add_parser('commit', help='adds a path to the current index')
    parser_commit.add_argument('-m', type=str, help='commit string')
    parser_commit.set_defaults(func=commit)

    # create the parser for the "status" command
    parser_status = subparsers.add_parser('status', help='displays info about the current working index')
    parser_status.set_defaults(func=status)

    # create the parser for the "log" command
    parser_log = subparsers.add_parser('log', help='displays most recent commits')
    parser_log.set_defaults(func=log)

    # create the parser for the "diff" command
    parser_diff = subparsers.add_parser('diff', help='check the diff of the current index')
    parser_diff.set_defaults(func=diff)

    # create the parser for the "branch" command
    parser_branch = subparsers.add_parser('branch', help='commands for managing branches')
    parser_branch.add_argument('b', nargs="?", type=str, help='new branch to create')
    parser_branch.set_defaults(func=branch)

    # create the parser for the "checkout" command
    parser_checkout = subparsers.add_parser('checkout', help='switches the head branch')
    parser_checkout.add_argument('-b', help='flag to create a new branch', action='store_true')
    parser_checkout.add_argument('branch', type=str, help='branch name')
    parser_checkout.set_defaults(func=checkout)

    # create the parser for the "merge" command
    parser_merge = subparsers.add_parser('merge', help='merges the head branch with some other branch')
    parser_merge.add_argument('branch', type=str, help='name of branch to merge')
    parser_merge.set_defaults(func=merge)

    # create the parser for the "push" command
    parser_push = subparsers.add_parser('push', help='uploads the local repository to the remote repository')
    parser_push.set_defaults(func=push)

    # create the parser for the "pull" command
    parser_pull = subparsers.add_parser('pull', help='downloads the local repository from the remote repository')
    parser_pull.set_defaults(func=pull)

    args = parser.parse_args()
    parser.parse_args()
    args.func(args)

def init(args):
    saga_repo = get_saga_repo_maybe()
    if saga_repo is not None:
        print("Error: saga project already exists at {}".format(saga_repo.base_directory))
    else:
        repository = Repository.init(os.getcwd())
        repository.write()
        print("Initialized empty saga repository in {}".format(repository.saga_directory))

def add(args):
    saga_repo = get_saga_repo()
    saga_repo.add(args.path)
    saga_repo.write()

def commit(args):
    saga_repo = get_saga_repo()
    if args.m is None:
        commit_message = input("Please enter a commit message: ")
        saga_repo.commit(commit_message)
    else:
        saga_repo.commit(args.m)
    saga_repo.write()

def status(args):
    saga_repo = get_saga_repo()
    saga_repo.status()

def log(args):
    saga_repo = get_saga_repo()
    saga_repo.log()

def diff(args):
    get_saga_repo().diff()

def branch(args):
    saga_repo = get_saga_repo()
    if args.b is not None:
        saga_repo.create_branch(args.b)
    saga_repo.branch()
    saga_repo.write()

def checkout(args):
    saga_repo = get_saga_repo()
    if args.b:
        saga_repo.create_branch(args.branch)
    saga_repo.switch_to_branch(args.branch)
    saga_repo.write()

def merge(args):
    saga_repo = get_saga_repo()
    saga_repo.merge(args.branch)
    saga_repo.write()

def push(args):
    print("PUSHING")
    saga_repo = get_saga_repo()
    saga_repo.push()

def pull(args):
    saga_repo = get_saga_repo()
    saga_repo.pull()
    saga_repo = get_saga_repo()
    saga_repo.restore_state_to_head()

# Helper functions

def get_saga_repo():
    saga_repo = get_saga_repo_maybe()
    if saga_repo is None:
        print("Error: command cannot run as no saga repo exists")
        exit(1)
    else:
        return saga_repo

def get_saga_repo_maybe():
    path = os.getcwd()
    while path != "/":
        # check if there is a
        if os.path.isdir(path + "/.saga"):
            return Repository.read(path) 
        path = os.path.dirname(path)
    return None

if __name__ == "__main__":
    main()
