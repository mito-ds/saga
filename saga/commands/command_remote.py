from saga.commands.utils import get_saga_repo1

def command_remote(args):
    saga_repo = get_saga_repo1()
    if args.remote is None:
        print(f"Remote branch is {saga_repo.remote_repository}")
    else:
        saga_repo.set_remote(args.remote)
