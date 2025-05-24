from functools import wraps
from http import HTTPStatus

from flask_jwt_extended import get_jwt_identity

from src.models.user import User


def requires_role(role_name):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            current_user = get_jwt_identity()
            user = User.query.filter_by(id=current_user).first()
            if user.role.name != role_name:
                return {"message": "Unauthorized"}, HTTPStatus.UNAUTHORIZED
            return f(*args, **kwargs)

        return wrapped

    return decorator
