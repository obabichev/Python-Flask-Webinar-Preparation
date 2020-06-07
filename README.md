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