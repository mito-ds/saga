from saga.operations.commit import commit
from saga.commands.utils import get_repository


def command_commit(args):
    repository = get_repository()
    if args.m is None:
        args.m = input("Please enter a commit message: ")
    commit(repository, args.m, allow_empty=args.allow_empty)
