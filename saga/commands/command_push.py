from saga.commands.utils import get_repository
from saga.operations.push import push

def command_push(args):
    repository = get_repository()
    push(repository)
