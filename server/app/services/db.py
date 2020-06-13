from flask_sqlalchemy import SQLAlchemy
from app.services.app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../../database.db'
db = SQLAlchemy(app)

from app.models.graph import Graph

db.create_all()
