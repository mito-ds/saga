from saga.Repository import Repository
from saga.operations.get_remote import get_remote

def pull(repository: Repository):
    url = f"{repository.remote_repository}/{repository.base_directory.name}.saga"
    get_remote(url)
    print(f"Got remote from {url}")
