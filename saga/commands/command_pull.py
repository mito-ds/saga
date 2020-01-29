from saga.commands.utils import get_saga_repo
from saga.operations.pull import pull

def command_pull(args):
    saga_repo = get_saga_repo()
    pull(saga_repo)
