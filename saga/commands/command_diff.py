from saga.commands.utils import get_repository
from saga.operations.diff import diff


def command_diff(args):
    repository = get_repository()
    diff(repository)
