from saga.commands.utils import get_saga_repo


def command_log(args):
    saga_repo = get_saga_repo()
    saga_repo.log()
