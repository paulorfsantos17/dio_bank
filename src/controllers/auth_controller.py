from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import create_access_token

from src.app import bcrypt
from src.models import User

app = Blueprint("auth", __name__, url_prefix="/auth")


def _check_password(password_hash, password_raw):
    return bcrypt.check_password_hash(password_hash, password_raw)


@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(username=username).first()
    is_password_valid = _check_password(user.password, password)

    if not user or is_password_valid is False:
        return {"msg": "Bad username or password"}, HTTPStatus.UNAUTHORIZED

    access_token = create_access_token(identity=str(user.id))
    return {"access_token": access_token}
