from flask import Flask
from flask_restx import Api
from models import Recipe, User
from exts import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from recipes import recipe_ns
from auth import auth_ns
from flask_cors import CORS


def create_app(config):
    app = Flask(__name__)         # Create the application instance
    app.config.from_object(config)

    CORS(app)                     # configuring the api to work on an application that is located on a different port

    db.init_app(app)              # Register sqlalchemy to work with our current app

    migrate = Migrate(app, db)
    JWTManager(app)

    api = Api(app, doc='/docs')   # Create an instance of the api, specify the current app to the Api class

    api.add_namespace(recipe_ns)  # the same as app.register_blueprint
    api.add_namespace(auth_ns)

    # After importing db instance, expose this via a terminal shell so that we can interact with our database object
    # model (serializer)
    @app.shell_context_processor
    def make_shell_context():
        return {
            "db":db,
            "Recipe":Recipe,
            "User":User
        }

    return app
