from saga.commands.utils import get_saga_repo1
from saga.operations.add import add

def command_add(args):
    saga_repo = get_saga_repo1()
    add(saga_repo, args.path)