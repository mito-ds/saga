from saga.commands.utils import get_saga_repo
from saga.operations.add import add


def command_add(args):
    saga_repo = get_saga_repo()
    add(saga_repo, args.path)
