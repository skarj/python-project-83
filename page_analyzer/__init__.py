import os

import psycopg2
from dotenv import load_dotenv
from flask import Flask

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


def get_db_connection():
    return psycopg2.connect(os.getenv('DB_URL'))


if True:
    import page_analyzer.controllers.urls_controller  # noqa: F401

__all__ = ["app"]
