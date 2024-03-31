from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import app_config
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(app_config)

db = SQLAlchemy(app)

from .models import Transport

with app.app_context():
    db.create_all()

from app import routes
