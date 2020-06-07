from flask import render_template

from app import app
from datetime import datetime

from app.models import User


@app.route('/')
def index():
    time = datetime.now()
    users = User.query.all()
    return render_template('index.html', time=time, users=users)
