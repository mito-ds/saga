from saga.commands.utils import get_repository
from saga.operations.list_branches import list_branches
from saga.operations.create_branch import create_branch


def command_branch(args):
    repository = get_repository()
    if args.b is not None:
        create_branch(repository, args.b)
    list_branches(repository)
