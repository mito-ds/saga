from saga.commands.utils import get_repository
from saga.operations.log import log

def command_log(args):
    repository = get_repository()
    log(repository)
