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

