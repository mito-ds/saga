from typing import Optional
from requests import Session
from getpass import getpass

def login(login_url: str) -> Optional[Session]:
    session = Session()

    # TODO: in the future, we can read these
    # from the global saga config file
    username = input("Username: ")
    password = getpass()

    try:
        session.post(
            login_url,
            data = {
                "username": username,
                "password": password
            }
        )
        
        return session
    except Exception:
        return None
