import os
from datetime import datetime

import click
import sqlalchemy as sa
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# Base declarativa para os modelos
class Base(DeclarativeBase):
    pass


# Instância global do SQLAlchemy usando a Base declarativa
db = SQLAlchemy(model_class=Base)


# Modelo de usuário
class User(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(sa.String, unique=True)
    email: Mapped[str] = mapped_column(sa.String, unique=True)
    active: Mapped[bool] = mapped_column(sa.Boolean, default=True)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r})"


# Modelo de post
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
            f"Post(id={self.id!r}, title={self.title!r}, author_id={self.author_id!r})"
        )


# Comando para inicializar o banco de dados
@click.command("init-db")
def init_db_command():
    """Clear the existing data and create new tables."""
    db.create_all()
    click.echo("Initialized the database.")


# Função factory para criar a aplicação Flask
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///blog.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    # Cria a pasta de instância, se necessário
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Rota de teste simples
    @app.route("/hello")
    def hello():
        return "Hello, World!"

    # Inicializa extensões
    db.init_app(app)
    Migrate(app, db)

    # Registra comandos de CLI
    app.cli.add_command(init_db_command)

    # Registra blueprints
    from src.controllers import post_controller, user_controller

    app.register_blueprint(user_controller.app)
    app.register_blueprint(post_controller.app)

    return app
