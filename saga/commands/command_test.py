import requests
import zipfile
from os import remove
from getpass import getpass

def command_test(args):
    s = requests.Session()

    username = input("Username: ")
    password = getpass()

    s.post(
        "http://localhost:3000/login",
        data = {
            "username": username,
            "password": password
        }
    )
    url = "http://localhost:3000/cli/pull/saga"

    with s.get(url, stream=True) as response:
        # throw an error, if there is wone
        response.raise_for_status()
        with open("sagatmp.zip", 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)

    with zipfile.ZipFile("sagatmp.zip", 'r') as zip_ref:
        zip_ref.extractall()
    remove("sagatmp.zip")