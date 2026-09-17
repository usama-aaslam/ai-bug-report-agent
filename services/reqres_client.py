import os

import requests


BASE_URL = "https://reqres.in/api"


def get_users():
    api_key = os.getenv("REQRES_API_KEY")

    if not api_key:
        raise RuntimeError(
            "REQRES_API_KEY is missing. "
            "Add it to your .env file."
        )

    headers = {
        "x-api-key": api_key,
    }

    response = requests.get(
        f"{BASE_URL}/users",
        headers=headers,
        timeout=30,
    )

    return response