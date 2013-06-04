from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object('configs.exampleconfig')
app.config.from_envvar('KTBCONF_FILE')

db = SQLAlchemy(app)


def register_blueprints(app):
    from views import images
    app.register_blueprint(images)

register_blueprints(app)

if __name__ == '__main__':
    app.run()
