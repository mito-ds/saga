from saga.commands.utils import get_saga_repo


def command_diff(args):
    get_saga_repo().diff()
