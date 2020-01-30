import argparse
from saga.commands.command_add import command_add
from saga.commands.command_branch import command_branch
from saga.commands.command_checkout import command_checkout
from saga.commands.command_clone import command_clone
from saga.commands.command_commit import command_commit
from saga.commands.command_diff import command_diff
from saga.commands.command_init import command_init
from saga.commands.command_log import command_log
from saga.commands.command_merge import command_merge
from saga.commands.command_pull import command_pull
from saga.commands.command_push import command_push
from saga.commands.command_remote import command_remote
from saga.commands.command_status import command_status
from saga.commands.command_test import command_test


def create_saga_parser():
    # create the top-level saga parser
    parser = argparse.ArgumentParser(prog='saga')
    subparsers = parser.add_subparsers(help='sub-command help')

    # create the parser for the "init" command
    parser_init = subparsers.add_parser(
        'init',
        help='creates a new saga project in the current directory'
    )
    parser_init.set_defaults(func=command_init)

    # create the parser for the "add" command
    parser_add = subparsers.add_parser(
        'add',
        help='adds a path to the current index'
    )
    parser_add.add_argument(
        'path',
        type=str,
        help='the path to add to the index'
    )
    parser_add.set_defaults(func=command_add)

    # create the parser for the "commit" command
    parser_commit = subparsers.add_parser(
        'commit',
        help='adds a path to the current index'
    )
    parser_commit.add_argument(
        '--allow-empty',
        action='store_true',
        help='allow the commit to be empty'
    )
    parser_commit.add_argument('-m', type=str, help='commit string')
    parser_commit.set_defaults(func=command_commit)

    # create the parser for the "status" command
    parser_status = subparsers.add_parser(
        'status',
        help='displays info about the current working index'
    )
    parser_status.set_defaults(func=command_status)

    # create the parser for the "log" command
    parser_log = subparsers.add_parser(
        'log',
        help='displays most recent commits'
    )
    parser_log.set_defaults(func=command_log)

    # create the parser for the "diff" command
    parser_diff = subparsers.add_parser(
        'diff',
        help='check the diff of the current index'
    )
    parser_diff.set_defaults(func=command_diff)

    # create the parser for the "branch" command
    parser_branch = subparsers.add_parser(
        'branch',
        help='commands for managing branches'
    )
    parser_branch.add_argument(
        'b',
        nargs="?",
        type=str,
        help='new branch to create'
    )
    parser_branch.set_defaults(func=command_branch)

    # create the parser for the "checkout" command
    parser_checkout = subparsers.add_parser(
        'checkout',
        help='switches the head branch'
    )
    parser_checkout.add_argument(
        '-b',
        help='flag to create a new branch',
        action='store_true'
    )
    parser_checkout.add_argument('branch', type=str, help='branch name')
    parser_checkout.set_defaults(func=command_checkout)

    # create the parser for the "merge" command
    parser_merge = subparsers.add_parser(
        'merge',
        help='merges the head branch with some other branch'
    )
    parser_merge.add_argument(
        'branch',
        type=str,
        help='name of branch to merge'
    )
    parser_merge.set_defaults(func=command_merge)

    # create the parser for the "push" command
    parser_push = subparsers.add_parser(
        'push',
        help='uploads the local repository to the remote repository'
    )
    parser_push.set_defaults(func=command_push)

    # create the parser for the "pull" command
    parser_pull = subparsers.add_parser(
        'pull',
        help='downloads the local repository from the remote repository'
    )
    parser_pull.set_defaults(func=command_pull)

    # create the parser for the "clone" command
    parser_clone = subparsers.add_parser(
        'clone',
        help='downloads a new local repository from the remote repository'
    )
    parser_clone.add_argument(
        'clone_url',
        type=str,
        help='url of remote repository to clone'
    )
    parser_clone.set_defaults(func=command_clone)

    # create the parser for the "remote" command
    parser_remote = subparsers.add_parser(
        'remote',
        help='manage the remote repositories'
    )
    parser_remote.add_argument(
        'remote',
        nargs="?",
        type=str,
        help='repository to track'
    )
    parser_remote.set_defaults(func=command_remote)

    # JUST FOR TESTING!
    parser_test = subparsers.add_parser(
        'test',
    )
    parser_test.set_defaults(func=command_test)

    return parser
