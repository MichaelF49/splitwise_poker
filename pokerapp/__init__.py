from flask import Flask
from pokerapp.config import Config

app = Flask(__name__)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    from pokerapp.main.routes import main
    from pokerapp.auth.routes import auth
    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app
