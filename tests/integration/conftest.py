import pytest
from flask_jwt_extended import create_access_token

from src.app import Role, User, create_app, db


@pytest.fixture()
def app():
    app = create_app(environment="TESTING")

    with app.app_context():
        db.create_all()
        # other setup can go here

        yield app
        db.drop_all()
        # clean up / reset resources here

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def access_token():
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()

    user = User(username="admin", password="admin", email="test", role=role)
    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=str(user.id))  # Correção aqui
    headers = {"Authorization": f"Bearer {token}"}
    return headers
