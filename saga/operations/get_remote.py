import requests
import zipfile
from os import remove

def get_remote(remote_url: str, session=None):
    if session is not None:
        response = session.get(remote_url, stream=True)
    else:
        response = requests.get(remote_url, stream=True)

    # TODO: throw an error, if there is one?
    with open("sagatmp.zip", 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

    with zipfile.ZipFile("sagatmp.zip", 'r') as zip_ref:
        zip_ref.extractall()
    remove("sagatmp.zip")