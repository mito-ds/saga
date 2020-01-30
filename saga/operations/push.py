import os
import shutil
import requests
from saga.Repository import Repository

def push(repository: Repository):
    url = f"{repository.remote_repository}/cli/push/{repository.base_directory.name}"

    # first we zip the entire repository
    shutil.make_archive("sagatmp", 'zip', repository.base_directory)

    # then we send it across the wire
    with open("sagatmp.zip", 'rb') as f:
        requests.post(
            url,
            files={"file": f}
        )
    os.remove("sagatmp.zip")
    print(f"Pushed {repository.base_directory.name} to {repository.remote_repository}")