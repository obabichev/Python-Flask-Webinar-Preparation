from flask import render_template, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required

from app import app, db
from datetime import datetime

from app.forms import RegisterForm, LoginForm, CreatePostForm
from app.models import User, Post


@app.route('/')
def index():
    time = datetime.now()
    users = User.query.all()
    posts = Post.query.all()
    return render_template('index.html', time=time, users=users, posts=posts)


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect(url_for('login'))
        login_user(user, remember=True)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, owner=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_post.html', form=form)


@app.route('/post/<id>')
def post_page(id):
    post = Post.query.filter_by(id=int(id)).first()
    return render_template('post.html', post=post)
