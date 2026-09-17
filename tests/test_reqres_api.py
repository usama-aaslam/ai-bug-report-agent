from dotenv import load_dotenv

from services.reqres_client import get_users


load_dotenv()


def test_get_users():
    response = get_users()

    assert response.status_code == 201

    body = response.json()

    assert "data" in body