from saga.commands.utils import get_repository
from saga.operations.pull import pull

def command_pull(args):
    repository = get_repository()
    pull(repository)
