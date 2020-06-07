from flask import render_template, redirect, url_for

from app import app, db
from datetime import datetime

from app.forms import RegisterForm
from app.models import User


@app.route('/')
def index():
    time = datetime.now()
    users = User.query.all()
    return render_template('index.html', time=time, users=users)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('register.html', form=form)
