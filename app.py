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
        return f'''usuario: {self.usuario},
        nombre: {self.nombre}, 
        apellido_usuario: {self.apellido_usuario},
        sexo: {self.sexo},
        fecha: {self.fecha},
        pais: {self.pais},
        password: {self.password}'''


class Autor(db.Model):
    __tablename__ = 'autores'
    nombre_autor = db.Column(db.String, primary_key=True, unique=True)
    apellidos = db.Column(db.String, primary_key=True)
    apodo = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'''nombre_autor={self.nombre_autor}, 
        apellidos={self.apellidos}, 
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
    fecha_publicacion = db.Column(db.Date, nullable=False)
    editorial = db.Column(db.String, nullable=False)
    paginas = db.Column(db.Integer, nullable=False)
    genero = db.Column(db.String, db.ForeignKey('generos.nombre_genero'))
    generos = db.relationship("Genero")

    def _repr_(self):
        return f'''nombre_libro: {self.nombre_libro}, 
        autor: {self.autor}, 
        fecha_publicacion: {self.fecha_publicacion}, 
        editorial: {self.editorial}, 
        paginas: {self.paginas}''' 





db.create_all()



connection.commit()
cursor.close()
connection.close()

#controller
@app.route('/')
def index():
    return render_template('index.html', usuarios=Usuario.query.order_by('nombre').all(), generos=Genero.query.order_by('nombre_genero').all())

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/usuario/create', methods=['POST'])
def create_todo_post():
    error = False
    response = {}
    try:
        usuario = request.get_json()['usuario']
        nombre = request.get_json()['nombre']
        apellido_usuario = request.get_json()['apellido_usuario']
        sexo = request.get_json()['sexo']
        fecha = request.get_json()['fecha']
        pais = request.get_json()['pais']
        password = request.get_json()['password']

        todo = Usuario(usuario=usuario, nombre=nombre, apellido_usuario=apellido_usuario, sexo=sexo, fecha=fecha, pais=pais, password=password)
        db.session.add(todo)
        db.session.commit()
        response['usuario'] = usuario
        response['nombre'] = nombre
        response['apellido_usuario'] = apellido_usuario
        response['sexo'] = sexo
        response['fecha'] = fecha
        response['pais'] = pais
        response['password'] = password
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


@app.route('/usuarios/createnom', methods=['POST'])
def create_todo_post_usuario():
    error = False
    response = {}
    try:
        usuario = request.get_json()['usuario']
        todo = Usuario(usuario = usuario)
        db.session.add(todo)
        db.session.commit()
        response['usuario'] = usuario
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



#run
if __name__ == '__main__':
    app.run(debug=True, port=5000)
