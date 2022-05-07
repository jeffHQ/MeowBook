#Imports
from flask import (
    Flask,
    jsonify, 
    redirect, 
    render_template, 
    request, 
    url_for,
    abort
)
from flask_sqlalchemy import SQLAlchemy

from app import configure_routes

def test_base_route():
    app = Flask(__name__, template_folder='../templates')
    configure_routes(app)
    client = app.test_client()
    url = '/'

    response = client.get(url)
    assert response.status_code == 200

def test_libro_route():
    app = Flask(__name__, template_folder='../templates')
    configure_routes(app)
    client = app.test_client()
    url = '/libro'

    response = client.get(url)
    assert response.status_code == 200