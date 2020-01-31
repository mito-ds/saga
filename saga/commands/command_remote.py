from saga.commands.utils import get_repository


def command_remote(args):
    repository = get_repository()
    if args.remote is None:
        print(f"Remote branch is {repository.remote_repository}")
    else:
        repository.set_remote(args.remote)
