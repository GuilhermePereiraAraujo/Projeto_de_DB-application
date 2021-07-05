from operator import truediv
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from random import randint


app = Flask(__name__)

# banco de dados (DataBase):

user='jayarkaw'
password='o1H2lHCqTPTJF4CeHvftNSGiaaASfMch'
host='tuffi.db.elephantsql.com'
database='jayarkaw'

app.config['SQLALCHEMY_DATABASE_URI']= f'postgresql://{user}:{password}@{host}/{database}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

app.secret_key = 'shave-palavra'

db = SQLAlchemy(app)

# filmes db

class Cantadas(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    chamada = db.Column(db.String(255), nullable=False)
    paquera = db.Column(db.String(255), nullable=False)

    def __init__(self,chamada,paquera):
        self.chamada = chamada
        self.paquera = paquera

    @staticmethod
    def read_all():
        #Select * from filmes order by id asc#
        return Cantadas.query.order_by(Cantadas.id.asc()).all()

    @staticmethod
    def read_single(registro_id):
        # SQL = select * from filmes where id=1
        return Cantadas.query.get(registro_id)

    def save(self):
        db.session.add(self)
        db.session.commit()


    def update(self, new_data):
        self.chamada = new_data.chamada
        self.paquera = new_data.paquera
        self.save()

    def delete(self):
        db.session.delete(self)
        db.session.commit()



#create

@app.route('/create', methods = ('GET', 'POST'))
def create():
    id_atribuido = None

    if request.method == 'POST':
        form = request.form


        registro = Cantadas(form['nome'],form['imagem_url'])
        registro.save()

        id_atribuido= registro.id

    return render_template ('create.html',id_atribuido= id_atribuido)




# rotas

@app.route('/')

def index ():
    return render_template('index.html')


@app.route('/read')

def read_all():
    registros = Cantadas.read_all()

    return render_template('read_all.html',registros=registros)

# def read_random(registro_id):
#     registro= Filmes.read_all(registro_id)
#     print(registro)

# random = randint(0,10)


@app.route(f'/read/<registro_id>')
def read_single(registro_id):
    registro = Cantadas.read_all(registro_id)
    print(registro)

    return render_template('read_single.html', registro=registro)

#update

@app.route('/update/<registro_id>',methods =('GET','POST'))

def update(registro_id):
    sucesso = None
    registro = Cantadas.read_single(registro_id)

    if request.method == 'POST':
        form = request.form
        new_data = Cantadas(form['nome'], form['imagem_url'])
        registro.update(new_data)
        sucesso = True

    return render_template('update.html', registro = registro, sucesso= sucesso)

#delete

@app.route('/delete/<registro_id>')


def delete(registro_id):

    registro = Cantadas.read_single(registro_id)

    return render_template('delete.html', registro = registro)

@app.route('/delete/<registro_id>/confirmed')

def delete_confirmed(registro_id):
    sucesso = None

    registro = Cantadas.read_single(registro_id)

    if registro:
        registro.delete()
        sucesso = True

    return render_template('delete.html', registro=registro, registro_id=registro_id, sucesso=sucesso)




if __name__ =='__main__':
    app.run(debug=True)