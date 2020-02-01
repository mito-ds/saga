import os
import shutil
import requests
from saga.Repository import Repository
from saga.operations.login import login

def push(repository: Repository):
    session = login(f"{repository.remote_repository}/login")

    if session is None:
        print("Login failed. Quiting")
        exit(1)

    url = f"{repository.remote_repository}/{repository.base_directory.name}.saga"

    # label it a tmp file
    tmp_zip_file = repository.base_directory.parent / "saga_tmp_zip"

    # first we zip the entire repository
    shutil.make_archive(tmp_zip_file, 'zip', repository.base_directory)

    # then we send it across the wire
    with open(f"{tmp_zip_file}.zip", 'rb') as f:
        session.post(
            url,
            files={"file": f}
        )
    os.remove(f"{tmp_zip_file}.zip")
    print(f"Pushed {repository.base_directory.name} to {repository.remote_repository}")