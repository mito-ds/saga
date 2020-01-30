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
        r = session.post(
            login_url,
            data = {
                "username": username,
                "password": password
            }
        )

        if r.status_code == 200:
            return session
        # login failed
        return None
    except Exception:
        return None
