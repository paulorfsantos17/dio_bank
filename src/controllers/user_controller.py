from http import HTTPStatus

from flask import Blueprint, request
from sqlalchemy import inspect

from src.app import User, db

app = Blueprint("user", __name__, url_prefix="/users")


def _create_user():
    data = request.json

    user = User(
        username=data["username"],
        email=data["email"],
    )
    db.session.add(user)
    db.session.commit()


def _list_users():
    query = db.select(User)
    results = db.session.execute(query).scalars()
    return [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }
        for user in results
    ]


@app.route("/", methods=["GET", "POST"])
def handle_user():
    if request.method == "POST":
        _create_user()
        return {"message": "User created"}, HTTPStatus.CREATED
    else:
        return {"users": _list_users()}, HTTPStatus.OK


@app.route("/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = db.get_or_404(User, user_id)
    return {"id": user.id, "username": user.username, "email": user.email}


@app.route("/<int:user_id>", methods=["PATCH"])
def update_user(user_id):
    user = db.get_or_404(User, user_id)
    data = request.json
    # if "username" in data:
    #     user.username = data["username"]
    #     db.session.commit()

    mapper = inspect(user)
    for column in mapper.attrs:
        if column.key in data:
            setattr(user, column.key, data[column.key])

    db.session.commit()

    return {"message": "User updated"}, HTTPStatus.OK


@app.route("/<int:user_id>", methods=["DELETE"])
def remove_user(user_id):
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()

    return "", HTTPStatus.NO_CONTENT
