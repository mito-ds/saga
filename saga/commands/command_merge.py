from saga.commands.utils import get_repository
from saga.operations.merge import merge


def command_merge(args):
    repository = get_repository()
    merge(repository, args.branch)
