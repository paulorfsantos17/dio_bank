from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import inspect

from src.app import bcrypt, db
from src.models import User

app = Blueprint("user", __name__, url_prefix="/users")
from src.utils.requires_roles import requires_role


def _create_user():
    data = request.json
    passwordHash = bcrypt.generate_password_hash(data["password"])

    user = User(
        username=data["username"],
        email=data["email"],
        password=passwordHash,
        role_id=1,
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
@jwt_required()
@requires_role("admin")
def handle_user():
    if request.method == "POST":
        _create_user()
        return {"message": "User created"}, HTTPStatus.CREATED
    else:
        return {"users": _list_users()}, HTTPStatus.OK


@app.route("/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user(user_id):
    current_user = get_jwt_identity()
    user = db.get_or_404(User, user_id)
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": {
            "name": user.role.name,
            "role_id": user.role_id,
        },
        "current_user": current_user,
    }


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
