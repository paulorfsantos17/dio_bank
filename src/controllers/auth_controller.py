from http import HTTPStatus

from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from sqlalchemy import inspect

from src.app import User, db

app = Blueprint("auth", __name__, url_prefix="/auth")


@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(username=username).first()

    if not user or password != user.password:
        return {"msg": "Bad username or password"}, HTTPStatus.UNAUTHORIZED

    access_token = create_access_token(identity=str(user.id))
    return {"access_token": access_token}
