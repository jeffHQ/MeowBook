# Imports
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
from datetime import datetime, timedelta

import psycopg2

# Configurations
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Magdalena150@localhost:5432/proyectodb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models:
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    apellido = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    usuario = db.Column(db.String(20), nullable=False, unique=True)
    contraseña = db.Column(db.String(80), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def _repr_(self):
        return f'''id: {self.id}, nombre: {self.nombre}, apellido: {self.apellido}, email: {self.email}, usuario: {self.usuario},
         contraseña: {self.contraseña} admin: {self.admin}.\n'''


class Autor(db.Model):
    __tablename__ = 'autores'
    nombre_autor = db.Column(db.String, primary_key=True, unique=True)
    apodo = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'''nombre_autor={self.nombre_autor}, 
        apodo={self.apodo}'''

class Genero(db.Model):
    __tablename__='generos'
    nombre_genero = db.Column(db.String, primary_key=True)

    def _repr_(self):
        return f'''nombre_genero: {self.nombre_genero}'''

class Libro(db.Model):
    __tablename__='libros'
    nombre_libro = db.Column(db.String, primary_key=True)

    autor = db.Column(db.String, db.ForeignKey('autores.nombre_autor'))
    autores = db.relationship("Autor")

    fecha_publicacion = db.Column(db.String, nullable=False)
    editorial = db.Column(db.String, nullable=False)
    paginas = db.Column(db.Integer, nullable=False)

    genero = db.Column(db.String, db.ForeignKey('generos.nombre_genero'))
    generos = db.relationship("Genero")

    sinopsis = db.Column(db.String, nullable=False)
    imagen = db.Column(db.String, nullable=False)

    def _repr_(self):
        return f'''nombre_libro: {self.nombre_libro}, 
        autor: {self.autor}, 
        fecha_publicacion: {self.fecha_publicacion}, 
        editorial: {self.editorial}, 
        paginas: {self.paginas},
        genero: {self.genero},
        sinopsis: {self.sinopsis},
        imagen: {self.imagen}''' 

connection = psycopg2.connect('dbname=proyectodb user=postgres host=localhost password=Magdalena150 port=5432')
cursor = connection.cursor()




connection.commit()
cursor.close()
connection.close()

db.create_all()
# Controllers:
@app.route('/')
def index():
    return redirect(url_for('login_menu'))


# MENU DE INICIO DE SESION
@app.route('/login')
def login_menu():
    return render_template('login.html')

@app.route('/login/succesful', methods=['POST'])
def login():
    email_in = request.form.get('email')
    contraseña_in = request.form.get('contraseña')
    first = Usuario.query.filter_by(email=email_in).first()
    if first is not None:
        if email_in == first.email:
            if contraseña_in == first.contraseña:
                return redirect(url_for('main_menu'))
            else:
                data = 'contraseña incorrecta'
                return render_template('login.html', data=data)
        else:
            data = 'el email no existe'
            return render_template('login.html', data=data)
    else:
        data = 'el email no existe'
        return render_template('login.html', data=data)

# MENU DE REGISTRO DE CUENTA
@app.route('/registro')
def signin_menu():
    return render_template('registro.html')

@app.route('/registro/succesful', methods=['POST'])
def registrarse():
    nombre_in = request.form.get('nombre')
    apellido_in = request.form.get('apellido')
    email_in = request.form.get('email')
    usuario_in = request.form.get('usuario')
    contraseña_in = request.form.get('contraseña')
    email_const = Usuario.query.filter_by(email=email_in).first()
    user_const = Usuario.query.filter_by(usuario=usuario_in).first()
    if email_const is not None:
        if email_in == email_const.email:
                data_1 = 'Email ya registrado'
                return render_template('registro.html', data_1=data_1) 
    if  user_const is not None:        
        if usuario_in == user_const.usuario:
                data_2 = 'Usuario ya existe'
                return render_template('registro.html', data_2=data_2)

    new_user = Usuario(nombre=nombre_in, apellido=apellido_in, email=email_in, usuario=usuario_in, contraseña=contraseña_in)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('main_menu'))

# MENU DE Libro
@app.route('/libro')
def libro_menu():
    return render_template('libro.html', libros=Libro.query.order_by('nombre_libro').all(), generos=Genero.query.order_by('nombre_genero').all(), autores=Autor.query.order_by('nombre_autor').all())

@app.route('/libro/registrar', methods=['POST'])
def create_libro_post():
    error = False
    response = {}
    try:
        nombre_libro = request.get_json()['nombre']
        autor = request.get_json()['autor']
        editorial = request.get_json()['editorial']
        fecha_publicacion = request.get_json()['año_publicacion']
        paginas = request.get_json()['nro_paginas']
        genero = request.get_json()['genero']
        sinopsis = request.get_json()['sinopsis']
        imagen = request.get_json()['imagen']
        libro = Libro(nombre_libro=nombre_libro, autor=autor, fecha_publicacion=fecha_publicacion, editorial=editorial, paginas=paginas, genero=genero, sinopsis=sinopsis, imagen=imagen)
        db.session.add(libro)
        db.session.commit()
        response['nombre_libro'] = nombre_libro
        response['autor'] = autor
        response['fecha_publicacion'] = fecha_publicacion
        response['editorial'] = editorial
        response['paginas'] = paginas
        response['genero'] = genero
        response['sinopsis'] = sinopsis
        response['imagen'] = imagen
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return jsonify(response)

@app.route('/libros/<libro_name>/delete-libro', methods=['DELETE'])
def delete_libro(libro_name):
    response = {}
    try:
        libro = Libro.query.get(libro_name)
        db.session.delete(libro)
        db.session.commit()
        response['success'] = True
    except:
        response['success'] = False
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify(response)


@app.route('/libro/busqueda', methods=['POST'])
def libro_busqueda():
    error = False
    respuesta = {}
    try:
        searchFieldx = request.get_json()['searchFieldx']
        
        connection = psycopg2.connect('dbname=proyectodb user=postgres host=localhost password=Magdalena150 port=5432')
        cursor = connection.cursor()
        SQL_SELECT = f'SELECT * from libros where nombre_libro like \'%{searchFieldx}%\' ;'

        cursor.execute(SQL_SELECT)
        respuesta = cursor.fetchall()
        
        
        
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        
        return jsonify(respuesta)


@app.route('/main_menu')
def main_menu():
    return render_template('main_menu.html', libros=Libro.query.order_by('nombre_libro').all())

@app.route('/editarlibro')
def editarlibro():
    return render_template('editar_libro.html', libros=Libro.query.order_by('nombre_libro').all(), generos=Genero.query.order_by('nombre_genero').all(), autores=Autor.query.order_by('nombre_autor').all())

@app.route('/libro/editar', methods=['POST'])
def editar_libro():
    error = False
    respuesta = {}
    try:
        eleccionlibro = request.get_json()['eleccionlibro']


        connection = psycopg2.connect('dbname=proyectodb user=postgres host=localhost password=Magdalena150 port=5432')
        cursor = connection.cursor()
        SQL_SELECT = f'SELECT * from libros where nombre_libro = \'{eleccionlibro}\';'
        
        
        cursor.execute(SQL_SELECT)
        respuesta = cursor.fetchall()
        

        
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return jsonify(respuesta)

@app.route('/libro/editar/final', methods=['POST'])
def libro_editar_final():
    error = False
    response = {}
    try:
        nombre_seguro = request.get_json()['libro_editar']
        name = request.get_json()['nombre_libro']
        autor = request.get_json()['autor']
        editorial = request.get_json()['editorial']
        fecha_publicacion = request.get_json()['año_publicacion']
        paginas = request.get_json()['nro_paginas']
        genero = request.get_json()['genero']
        sinopsis = request.get_json()['sinopsis']
        imagen = request.get_json()['imagen']
        
        
        book = db.session.query(Libro).get(nombre_seguro)
        print(nombre_seguro)
        print(book)

        book.nombre_libro = name
        book.autor = autor
        book.editorial = editorial
        book.año_publicacion = fecha_publicacion
        book.nro_paginas = paginas
        book.paginas = paginas
        book.genero = genero
        book.sinopsis = sinopsis
        book.imagen = imagen

        db.session.commit()

        

    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return jsonify(response)


#-----------------------------------------------------------------------------------------

@app.errorhandler(404)
def pagina_no_existe(e):
    return render_template('404.html'), 404

#-----------------------------------------------------------------------------------------

# Run:
if __name__ == '__main__':
    app.run(debug=True, port=5003)