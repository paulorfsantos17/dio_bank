from http import HTTPStatus

from flask_jwt_extended import create_access_token

from src.app import Role, User, db


def test_get_user_sucess(client, access_token):
    headers = access_token

    response = client.get("users/1", headers=headers)

    assert response.status_code == HTTPStatus.OK
    assert response.json["username"] == "admin"


def test_list_user_sucess(client, access_token):
    headers = access_token

    response = client.get("users/", headers=headers)

    assert response.status_code == HTTPStatus.OK

    users = response.get_json()
    breakpoint()
    assert len(users) == 1
    assert users["users"][0]["username"] == "admin"


def test_create_user_sucess(client, access_token):

    headers = access_token
    body = {
        "username": "new user",
        "email": "new user",
        "password": "new user",
        "role_id": 1,
    }

    response = client.post("users/", headers=headers, json=body)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json["message"] == "User created"

    users_database = User.query.all()
    assert len(users_database) == 2
    assert users_database[1].username == "new user"
