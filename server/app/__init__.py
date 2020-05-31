from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .controllers import controllers as controllers_blueprint
from .services import services as services_blueprint

app = Flask(__name__)
db = SQLAlchemy()

app.register_blueprint(services_blueprint)
app.register_blueprint(controllers_blueprint)
