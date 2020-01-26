from saga.commands.utils import get_saga_repo


def command_status(args):
    saga_repo = get_saga_repo()
    saga_repo.status()
