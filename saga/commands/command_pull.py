from saga.commands.utils import get_saga_repo

def command_pull(args):
    saga_repo = get_saga_repo()
    saga_repo.pull()
    saga_repo = get_saga_repo()
    saga_repo.restore_state_to_head()
