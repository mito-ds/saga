from saga.commands.utils import get_saga_repo1
from saga.operations.merge import merge

def command_merge(args):
    saga_repo = get_saga_repo1()
    merge(saga_repo, args.branch)