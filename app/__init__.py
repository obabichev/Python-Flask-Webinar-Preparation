from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object('config.Config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import models
from app import routes
