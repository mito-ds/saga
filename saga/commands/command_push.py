from saga.commands.utils import get_saga_repo
from saga.operations.push import push

def command_push(args):
    saga_repo = get_saga_repo()
    push(saga_repo)
