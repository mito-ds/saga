import os
#from saga.commands.utils import get_saga_repo
from saga.operations.commit import commit
from saga.commands.utils import get_saga_repo1

def command_commit(args):
    saga_repo = get_saga_repo1()
    if args.m is None:
        args.m = input("Please enter a commit message: ")
    commit(saga_repo, args.m, allow_empty=args.allow_empty)