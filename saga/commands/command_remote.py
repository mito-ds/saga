from saga.commands.utils import get_saga_repo


def command_remote(args):
    saga_repo = get_saga_repo()
    if args.remote is None:
        print(f"Remote branch is {saga_repo.remote_repository}")
    else:
        saga_repo.set_remote(args.remote)
