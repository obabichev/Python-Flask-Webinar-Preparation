from datetime import datetime

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    time = datetime.now()
    return render_template('index.html', time=time)
