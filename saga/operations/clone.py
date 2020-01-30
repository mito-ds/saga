from saga.operations.get_remote import get_remote

def clone(clone_url: str):
    get_remote(clone_url)
    print(f"Cloned {clone_url}")
