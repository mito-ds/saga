from saga.commands.utils import get_repository

def command_state_hash(args):
    repository = get_repository()
    print(repository.get_state_hash(args.branch))
