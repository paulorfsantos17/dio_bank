import os
from datetime import datetime

import click
import sqlalchemy as sa
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class User(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(sa.String, unique=True)
    email: Mapped[str] = mapped_column(sa.String, unique=True)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.name!r})"


class Post(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    title: Mapped[str] = mapped_column(sa.String, nullable=False)
    body: Mapped[str] = mapped_column(sa.String, nullable=False)
    created: Mapped[datetime] = mapped_column(
        sa.DateTime, nullable=False, server_default=sa.func.now()
    )
    author_id: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey("user.id"))

    def __repr__(self) -> str:
        return (
            f"Post(id={self.id!r}, title={self.name!r}, author_id={self.author_id!r})"
        )


@click.command("init-db")
def init_db_command():
    """Clear the existing data and create new tables."""
    global db
    with current_app.app_context():
        db.create_all()
    click.echo("Initialized the database.")


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///blog.db",
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route("/hello")
    def hello():
        return "Hello, World!"

    # registration of commands
    app.cli.add_command(init_db_command)

    # inilialize extenstions
    db.init_app(app)

    return app
