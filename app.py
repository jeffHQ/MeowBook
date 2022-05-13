#imports
#from crypt import methods
from email.policy import default
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
import psycopg2

#configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Magdalena150@localhost:5432/proyectodb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


connection = psycopg2.connect('dbname=proyectodb user=postgres host=localhost password=Magdalena150 port=5432')
cursor = connection.cursor()

db = SQLAlchemy(app)
migrate = Migrate(app, db)

#models

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    nombre_usuario = db.Column(db.String(), nullable=False)
    apellido_usuario = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    usuario = db.Column(db.String(), primary_key=True)
    contraseña = db.Column(db.String(), nullable=False)

    
    
    def __repr__(self):
        return f'''nombre_usuario: {self.nombre_usuario}, 
        apellido_usuario: {self.apellido_usuario},
        email: {self.email},
        usuario: {self.usuario},
        contraseña: {self.contraseña}'''


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
    editorial = db.Column(db.String, nullable=False)
    año_publicacion = db.Column(db.Integer, nullable=False)
    nro_paginas = db.Column(db.Integer, nullable=False)
    genero = db.Column(db.String, db.ForeignKey('generos.nombre_genero'))
    generos = db.relationship("Genero")
    sinopsis = db.Column(db.String, nullable=False)
    imagen = db.Column(db.String, nullable=False)
    def _repr_(self):
        return f'''nombre_libro: {self.nombre_libro}, 
        autor: {self.autor}, 
        editorial: {self.editorial}, 
        año_publicacion: {self.año_publicacion}, 
        nro_paginas: {self.nro_paginas},
        genero: {self.genero},
        imagen: {self.imagen}''' 





db.create_all()



connection.commit()
cursor.close()
connection.close()

#controller
@app.route('/')
def index():
    return render_template('index.html', usuarios=Usuario.query.order_by('nombre_usuario').all(), generos=Genero.query.order_by('nombre_genero').all())

@app.route('/editarlibro')
def editarlibro():
    return render_template('editar_libro.html', libros=Libro.query.order_by('nombre_libro').all())

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/registro_usuario')
def registro_usuario():
    return render_template('registro_usuario.html')

@app.route('/mainmenu')
def mainmenu():
    return render_template('mainmenu.html', libros=Libro.query.order_by('nombre_libro').all())


@app.route('/registro_libro')
def registro_libro():
    return render_template('registro_libro.html', generos=Genero.query.order_by('nombre_genero').all(), autores=Autor.query.order_by('nombre_autor').all())
    
@app.route('/usuario/create', methods=['POST'])
def create_todo_post():
    error = False
    response = {}
    try:
        
        nombre_usuario = request.get_json()['nombre_usuario']
        apellido_usuario = request.get_json()['apellido_usuario']
        email = request.get_json()['email']
        usuario = request.get_json()['usuario']
        contraseña = request.get_json()['contraseña']

        user = Usuario(nombre_usuario=nombre_usuario, apellido_usuario=apellido_usuario, email=email, usuario=usuario,contraseña=contraseña)
        db.session.add(user)
        db.session.commit()
        response['nombre_usuario'] = nombre_usuario
        response['apellido_usuario'] = apellido_usuario
        response['email'] = email
        response['usuario'] = usuario
        response['contraseña'] = contraseña
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

@app.route('/libro/registrar', methods=['POST'])
def registrar_libro():
    error = False
    respuesta = {}
    try:
        nombre_libro = request.get_json()['nombre_libro']
        autor = request.get_json()['autor']
        editorial = request.get_json()['editorial']
        año_publicacion = request.get_json()['año_publicacion']
        nro_paginas = request.get_json()['nro_paginas']
        genero = request.get_json()['genero']
        sinopsis = request.get_json()['sinopsis']
        imagen = request.get_json()['imagen']
        libro = Libro(nombre_libro=nombre_libro,
                    autor=autor,
                    editorial=editorial,
                    año_publicacion=año_publicacion,
                    nro_paginas=nro_paginas,
                    genero=genero,
                    sinopsis=sinopsis,
                    imagen=imagen)
        db.session.add(libro)
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
        return jsonify(respuesta)


@app.route('/libro/editar', methods=['POST'])
def editar_libro():
    error = False
    respuesta = {}
    try:
        eleccionlibro = request.get_json()['eleccionlibro']


        connection = psycopg2.connect('dbname=proyectodb user=postgres host=localhost password=Magdalena150 port=5432')
        cursor = connection.cursor()
        SQL_SELECT = f'SELECT * from libros where nombre_libro = \'{eleccionlibro}\';'
        
        print(SQL_SELECT)
        cursor.execute(SQL_SELECT)
        respuesta = cursor.fetchall()
        print("a")
        print(respuesta)

        
        db.session.add(libro)
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
        return jsonify(respuesta)


#run
if __name__ == '__main__':
    app.run(debug=True, port=5000)
