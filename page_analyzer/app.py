from flask import Flask, render_template
from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)

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
        'show.html'
    )


@app.post('/urls')
def urls_add():
    return render_template(
        'index.html'
    )
