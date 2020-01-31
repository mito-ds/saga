from saga.commands.utils import get_repository
from saga.operations.add import add


def command_add(args):
    repository = get_repository()
    add(repository, args.path)
