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
    usuario = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String(), nullable=False)
    apellidos = db.Column(db.String(), nullable=False)
    sexo = db.Column(db.String(), nullable=False)
    fecha = db.Column(db.Date(), nullable=False)
    pais = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    
    



    def __repr__(self):
        return f'Usuario: usuario={self.usuario}, nombre={self.nombre}'


db.create_all()
SQL_INSERT = 'insert into usuarios(usuario, nombre, apellidos, sexo, fecha, pais, password) values(%(usuario)s, %(nombre)s, %(apellidos)s, %(sexo)s, %(fecha)s, %(pais)s, %(password)s)'


connection.commit()
cursor.close()
connection.close()

#controller
@app.route('/')
def index():
    return render_template('index.html', usuarios=Usuario.query.order_by('nombre').all())

@app.route('/usuarios/create', methods=['POST'])
def create_todo_post():
    error = False
    response = {}
    try:
        usuario = request.get_json()['usuario']
        nombre = request.get_json()['nombre']
        apellidos = request.get_json()['apellidos']
        sexo = request.get_json()['sexo']
        fecha = request.get_json()['fecha']
        pais = request.get_json()['pais']
        password = request.get_json()['password']

        todo = Todo(usuario=usuario, nombre=nombre, apellidos=apellidos, sexo=sexo, fecha=fecha, pais=pais, password=password)
        db.session.add(todo)
        db.session.commit()
        response['usuario'] = usuario
        response['nombre'] = nombre
        response['apellidos'] = apellidos
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
        todo = Todo(usuario = usuario)
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