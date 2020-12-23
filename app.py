from flask import Flask,url_for,flash,session,render_template, request, redirect
from datetime import date, datetime
import sqlite3


app = Flask(__name__)
app.secret_key ='spbYO0JJ0PUFLUikKYbKrpS5w3KUEnab5KcYDdYb'
db = sqlite3.connect('data.db', check_same_thread=False)


@app.route('/', methods=['GET']) 
def index():

    entradas = db.execute("""select id_entrada,titulo,descripcion,autor,fecha from entradas""")
    return render_template('index.html', entradas=entradas)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    email = request.form.get('email')
    password = request.form.get('password')

    usuario =db.execute(""" select * from usuarios where email = ? and password = ? """,(email,password)).fetchone()
    if usuario is None:
        flash('datos incorrectos','badge bg-danger')
        return redirect(url_for('login'))
    session['usuario'] = usuario 
    return redirect(url_for('index'))

@app.route('/logout',methods=['GET','POST'])
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/entrada', methods=['GET', 'POST']) 
def entrada():
    if not 'usuario' in session:
        return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('entradas/crear.html')
    
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descripcion = request.form.get('descripcion')
        autor = request.form.get('autor')
        fecha = datetime.now()
        cursor = db.cursor()
        cursor.execute("""insert into entradas(
                titulo,
                descripcion,
                autor,
                fecha
            )values (?,?,?,?)
        """, (titulo,descripcion,autor,fecha))
        db.commit()
    return redirect(url_for('index'))


@app.route('/usuario', methods=['GET']) 
def usuario():
    return render_template('index.html')

@app.route('/login/usuario', methods=['GET', 'POST'])
def usuario_crear():
    if request.method == 'GET':
        return render_template('crear.html')

    if request.method == 'POST':
        nombres = request.form.get('nombres')
        email = request.form.get('email')
        password = request.form.get('password')

        cursor = db.cursor()
        cursor.execute("""insert into usuarios(
                nombres,
                email,
                password
            )values (?,?,?)
        """, (nombres, email, password))
        db.commit()
        flash("Usuario creado.","badge bg-success")
    return redirect(url_for('index'))

