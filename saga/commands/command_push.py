from saga.commands.utils import get_saga_repo


def command_push(args):
    print("PUSHING")
    saga_repo = get_saga_repo()
    saga_repo.push()
