from datetime import datetime

from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object('config.Config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import models


@app.route('/')
def index():
    time = datetime.now()
    return render_template('index.html', time=time)
