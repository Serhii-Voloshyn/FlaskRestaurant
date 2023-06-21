from flask import Flask

import click
from config import Config
from flask.cli import with_appcontext
from app.models import db


def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(config_class)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI=app.config["SQLALCHEMY_DATABASE_URI"],
        SQLALCHEMY_TRACK_MODIFICATIONS=app.config[
            "SQLALCHEMY_TRACK_MODIFICATIONS"
        ]
    )

    with app.app_context():
        db.init_app(app)

        from .views import routes
        app.register_blueprint(routes)

    app.cli.add_command(init_db_command)

    return app


def init_db():
    db.drop_all()
    db.create_all()


@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the database.")
