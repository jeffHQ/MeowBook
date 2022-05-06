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
from flask_migrate import Migrate
import sys

# Configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:1234@localhost:5432/proyectodb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) # Instancia de SQLAlchemy
migrate = Migrate(app, db) # Instancia de la aplicación + Instacia SQLAlchemy

# Models
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    email = db.Column(db.String(), primary_key=True)
    usuario = db.Column(db.String(), primary_key=True)
    contraseña = db.Column(db.String(), nullable=False)
    nombre = db.Column(db.String(), nullable=False)
    apellido = db.Column(db.String(), nullable=False)
    edad = db.Column(db.Date, nullable=False)
    admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'''email: {self.email},
         usuario: {self.usuario},
          contraseña: {self.contraseña},
          nombre: {self.nombre},
          apellido: {self.apellido},
          edad: {self.edad},
          admin: {self.admin}'''
          
class Libro(db.Model):
    __tablename_ = 'libros'
    nombre = db.Column(db.String(), primary_key = True)
    autor = db.Column(db.String(), nullable = False)
    editorial = db.Column(db.String(), nullable = False)
    año_publicacion = db.Column(db.Integer, nullable = False)
    nro_paginas = db.Column(db.Integer, nullable = False)
    genero = db.Column(db.String(), nullable = False )
    sinopsis = db.Column(db.String(), nullable = False)

    def __repr__(self):
        return f'nombre: {self.nombre}, autor: {self.autor}, editorial: {self.editorial}, año_publicacion: {self.año_publicacion}, nro_paginas: {self.nro_paginas}, genero: {self.genero}, sinopsis: {self.sinopsis}'

class Autor(db.Model):
    __tablename__ = 'autores'
    nombre = db.Column(db.String(80), primary_key=True)
    apellido = db.Column(db.String(80), primary_key=True)
    apodo = db.Column(db.String(80), nullable=True)
    
    def __repr__(self):
        return f'''nombre: {self.nombre},
         apellido: {self.apellido},
         apodo: {self.apodo}'''

#db.create_all()

#Controllers 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/libro')
def libro():
    return render_template('libro.html')

@app.route('/usuario/registrar', methods=['POST'])
def registrar_usuario():
    respuesta = {}
    try:
        nombre = request.get_json()['nombre']
        apellido = request.get_json()['apellido']
        edad = request.get_json()['edad']
        email = request.get_json()['email']
        usuario = request.get_json()['usuario']
        contraseña = request.get_json()['contraseña']
        user = Usuario(email=email,usuario=usuario,contraseña=contraseña,nombre=nombre,apellido=apellido,edad=edad)
        print(user)
        db.session.add(user)
        db.session.commit()
        respuesta['nombre'] = nombre
        respuesta['apellido'] = apellido
        respuesta['edad'] = edad
        respuesta['email'] = email
        respuesta['usuario'] = usuario
        respuesta['contraseña'] = contraseña
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify(respuesta)

@app.route('/libro/registrar', methods=['POST'])
def registrar_libro():
    respuesta = {}
    try:
        nombre = request.get_json()['nombre']
        autor = request.get_json()['autor']
        editorial = request.get_json()['editorial']
        año_publicacion = request.get_json()['año_publicacion']
        nro_paginas = request.get_json()['nro_paginas']
        genero = request.get_json()['genero']
        sinopsis = request.get_json()['sinopsis']
        libro = Libro(nombre=nombre,
                    autor=autor,
                    editorial=editorial,
                    año_publicacion=año_publicacion,
                    nro_paginas=nro_paginas,
                    genero=genero,
                    sinopsis=sinopsis)
        db.session.add(libro)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify(respuesta)
    
# Run
if __name__ == '__main__':
    app.run(debug=True, port=5003)