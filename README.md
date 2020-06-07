## Flask Webinar Roadmap

### Create the project

```shell script
mkdir project
cd project
python3 -m venv venv
source venv/bin/activate
```

### Create Flask instance

```python
# app/__init__.py
from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hallo world!!'
```

### Run dev server

```shell script

flask run

# Run with debug mode
FLASK_ENV=development flask run
```

### Create template

app/templates/index.html
```jinja2
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Flask Webinar Preparation</title>
</head>
<body>
<h2>Time</h2>
<p>
    {{ time }}
</p>
</body>
</html>
```

app/__init__.py
```python
#...

@app.route('/')
def index():
    time = datetime.now()
    return render_template('index.html', time=time)
```

### Database

```shell script
docker run -e POSTGRES_USER=test -e POSTGRES_PASSWORD=test -e POSTGRES_DB=test -p 5433:5432 -d postgres
```

### SQLAlchemy

```shell script
pip install flask-sqlalchemy
pip install flask-migrate
```

Config.py
```python
class Config:
    SQLALCHEMY_DATABASE_URI = 'postgres://test:test@localhost:5433/test'
```

app/__init__.py
```python
#...
app = Flask(__name__)

app.config.from_object('config.Config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
```

### Modeling

models.py
```python
from app import db


class User(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(256), unique=True, nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password_hash = db.Column(db.String(1024), nullable=False)
```

### Migrations

```shell script
flask db init
flask db migrate -m "User"
flask db upgrade

pip install psycopg2-binary
flask db upgrade
```

```sql
insert into public.user (username, email, password_hash)
values ('obabichev', 'babichev.oleg.n@gmail.com', '123123123');

select *
from public.user;
```

### Render users

routes.py
```python
from flask import render_template

from app import app
from datetime import datetime

from app.models import User


@app.route('/')
def index():
    time = datetime.now()
    users = User.query.all()
    return render_template('index.html', time=time, users=users)
```

templates/index.html
```html
<ul>
    {% for user in users %}
        <li>{{ user.username }} ({{ user.email }})</li>
    {% endfor %}
</ul>
```

### Register page

```shell script
pip install flask-login
pip freeze > requirements.txt
```

__init__
```python
login = LoginManager(app)
```

models.py
```python
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class User(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(256), unique=True, nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password_hash = db.Column(db.String(1024), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
```

```shell script
pip install flask-wtf
```

forms.py
```python
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError

from app.models import User


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('User with this username already exists')
```

routes.py
```python
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

```

register.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Flask Webinar Preparation</title>
</head>
<body>
<h2>Register</h2>
<form action="" method="post">
    {{ form.hidden_tag() }}
    <div>
        <div>{{ form.username.label }}</div>
        <div>{{ form.username() }}</div>
        <div>
            {% for error in form.username.errors %}
                <div>{{ error }}</div>
            {% endfor %}
        </div>
    </div>
    <div>
        <div>{{ form.email.label }}</div>
        <div>{{ form.email() }}</div>
        <div>
            {% for error in form.email.errors %}
                <div>{{ error }}</div>
            {% endfor %}
        </div>
    </div>
    <div>
        <div>{{ form.password.label }}</div>
        <div>{{ form.password(type='password') }}</div>
        <div>
            {% for error in form.password.errors %}
                <div>{{ error }}</div>
            {% endfor %}
        </div>
    </div>
    <div>{{ form.submit() }}</div>
</form>
</body>
</html>
```

### Login

forms
```python
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
```

route
```python

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
```

template
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Flask Webinar Preparation</title>
</head>
<body>
<h2>Login</h2>
<form action="" method="post">
    {{ form.hidden_tag() }}
    <div>
        <div>{{ form.username.label }}</div>
        <div>{{ form.username() }}</div>
        <div>
            {% for error in form.username.errors %}
                <div>{{ error }}</div>
            {% endfor %}
        </div>
    </div>
    <div>
        <div>{{ form.password.label }}</div>
        <div>{{ form.password(type='password') }}</div>
        <div>
            {% for error in form.password.errors %}
                <div>{{ error }}</div>
            {% endfor %}
        </div>
    </div>
    <div>{{ form.submit() }}</div>
</form>
</body>
</html>
```

### Logout

index.html
```html
{% if not current_user.is_anonymous %}
    <div>
        User: {{ current_user.username }} <a href="{{ url_for('logout') }}">Logout</a>
    </div>
{% endif %}
```

route
```python
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
```

