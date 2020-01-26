from saga.commands.utils import get_saga_repo1
from saga.operations.list_branches import list_branches
from saga.operations.create_branch import create_branch

def command_branch(args):
    saga_repo = get_saga_repo1()
    if args.b is not None:
        create_branch(saga_repo, args.b)
    list_branches(saga_repo)