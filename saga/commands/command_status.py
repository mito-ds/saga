from saga.commands.utils import get_repository
from saga.operations.status import status

def command_status(args):
    repository = get_repository()
    status(repository)
