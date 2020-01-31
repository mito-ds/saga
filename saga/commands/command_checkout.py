from saga.commands.utils import get_repository
from saga.operations.checkout import checkout
from saga.operations.create_branch import create_branch


def command_checkout(args):
    repository = get_repository()
    if args.b:
        create_branch(repository, args.branch)
    checkout(repository, args.branch)
