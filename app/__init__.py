from flask import Flask

from app.routes import main


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="tareas-app-local",
    )

    if test_config:
        app.config.update(test_config)

    app.register_blueprint(main)
    return app
