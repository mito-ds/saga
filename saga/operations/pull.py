import requests
import zipfile
from saga.Repository import Repository

def pull(repository: Repository):
    url = f"{repository.remote_repository}/cli/pull"

    with requests.get(url, stream=True) as response:
        # throw an error, if there is wone
        response.raise_for_status()
        with open("tmp.zip", 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    # f.flush()

    import os
    print(os.path.exists("tmp.zip"))
    with zipfile.ZipFile("tmp.zip", 'r') as zip_ref:
        print(f"WRITING to {repository.base_directory}")
        zip_ref.extractall(f"{repository.base_directory}")
    print("DONE")
