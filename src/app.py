import os

from flask import Flask, json
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from werkzeug.exceptions import HTTPException

from src.models.base import db

# Instância global do JWTManager
jwt = JWTManager()
bcrypt = Bcrypt()


# # Comando para inicializar o banco de dados
# @click.command("init-db")
# def init_db_command():
#     """Clear the existing data and create new tables."""
#     db.create_all()
#     click.echo("Initialized the database.")


# Função factory para criar a aplicação Flask
def create_app(environment=os.environ["ENVIRONMENT"]):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(f"src.config.{environment.title()}Config")
    # Cria a pasta de instância, se necessário
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Inicializa extensões
    db.init_app(app)
    Migrate(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # Registra comandos de CLI
    # app.cli.add_command(init_db_command)

    # Registra blueprints
    from src.controllers import (
        auth_controller,
        post_controller,
        role_controller,
        user_controller,
    )

    app.register_blueprint(user_controller.app)
    app.register_blueprint(post_controller.app)
    app.register_blueprint(auth_controller.app)
    app.register_blueprint(role_controller.app)

    @app.errorhandler(HTTPException)
    def handle_exception(e):
        """Return JSON instead of HTML for HTTP errors."""
        # start with the correct headers and status code from the error
        response = e.get_response()
        # replace the body with JSON
        response.data = json.dumps(
            {
                "code": e.code,
                "name": e.name,
                "description": e.description,
            }
        )
        response.content_type = "application/json"
        return response

    return app
