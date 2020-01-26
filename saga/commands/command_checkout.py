from saga.commands.utils import get_saga_repo1
from saga.operations.checkout import checkout
from saga.operations.create_branch import create_branch

def command_checkout(args):
    saga_repo = get_saga_repo1()
    if args.b:
        create_branch(saga_repo, args.branch)
    checkout(saga_repo, args.branch)