import os
import psycopg2
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


def get_db_connection():
    return psycopg2.connect(os.getenv('DB_URL'))


# Import controllers to register routes
import page_analyzer.controllers.urls_controller

__all__ = ["app"]
