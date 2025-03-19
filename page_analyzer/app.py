from flask import Flask, render_template
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template(
        'index.html'
    )


@app.get('/urls')
def urls_show():
    return render_template(
        'sites.html'
    )


@app.post('/urls')
def urls_add():
    return render_template(
        'index.html'
    )
