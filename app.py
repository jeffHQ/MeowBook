from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

from sqlalchemy import false, true

# Configuration
app = Flask('__name__')
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:1234@localhost:5432/todoapp20'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) # Instancia de SQLAlchemy
migrate = Migrate(app, db) # Instancia de la aplicación + Instacia SQLAlchemy

# Models
class Libro(db.Model):
    __tablename_ = 'libros'
    nombre = db.Column(db.string(80), primary_key=True)
    fecha_publicacion = db.Column(db.string(80), nullable=False)
    editorial = db.Column(db.String(80), nullable=False)
    nro_paginas = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return f'''nombre: {self.nombre},
         fecha: {self.fecha_publicacion},
          editorial: {self.editorial},
          nro_paginas: {self.nro_paginas}'''

class Autor(db.Model):
    __tablename__ = 'autores'
    nombre = db.Column(db.String(80), primary_key=True)
    apellido = db.Column(db.String(80), primary_key=True)
    apodo = db.Column(db.String(80), nullable=True)
    
    def __repr__(self):
        return f'''nombre: {self.nombre},
         apellido: {self.apellido},
         apodo: {self.apodo}'''