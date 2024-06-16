from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker, joinedload
from datetime import date
from Entity import Equipo, Posicion, Jugador, Base  # Importamos las nuevas entidades
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

app.secret_key = '123456789'
# Crear conexión a la base de datos
engine = create_engine('postgresql://postgres:123456789@localhost/futbol')
Base.metadata.bind = engine

# Crear sesión de base de datos
DBSession = sessionmaker(bind=engine)

# Ruta principal
@app.route("/")
def home():
    return render_template('index.html')

# Rutas para Equipo
@app.route('/equipo')
def listar_equipo():
    session = DBSession()
    equipos = session.query(Equipo).all()
    session.close()
    return render_template('equipo.html', equipos=equipos)

@app.route('/equipo/agregar', methods=['GET', 'POST'])
def agregar_equipo():
    if request.method == 'POST':
        session = DBSession()
        Equipo.agregarEquipo(session,
                             request.form['nombreequipo'],
                             request.form['anioofundacion'],
                             request.form['estadio'],
                             request.form['ciudad'])
        session.close()
        return redirect(url_for('listar_equipo'))
    else:
        return render_template('agregar_equipo.html')

@app.route('/equipo/editar/<int:idequipo>', methods=['GET', 'POST'])
def editar_equipo(idequipo):
    session = DBSession()
    if request.method == 'POST':
        Equipo.modificarEquipo(session, idequipo,
                               nombreequipo=request.form['nombreequipo'],
                               anioofundacion=request.form['anioofundacion'],
                               estadio=request.form['estadio'],
                               ciudad=request.form['ciudad'])
        session.close()
        return redirect(url_for('listar_equipo'))
    else:
        equipo = session.query(Equipo).filter_by(idequipo=idequipo).first()
        session.close()
        return render_template('editar_equipo.html', equipo=equipo)

@app.route('/equipo/eliminar/<int:idequipo>', methods=['POST'])
def eliminar_equipo(idequipo):
    session = DBSession()
    Equipo.eliminarEquipo(session, idequipo)
    session.close()
    return redirect(url_for('listar_equipo'))

# Rutas para Posicion
@app.route('/posicion')
def listar_posicion():
    session = DBSession()
    posiciones = session.query(Posicion).all()
    session.close()
    return render_template('posicion.html', posiciones=posiciones)

@app.route('/posicion/agregar', methods=['GET', 'POST'])
def agregar_posicion():
    if request.method == 'POST':
        session = DBSession()
        Posicion.agregarPosicion(session,
                                 request.form['nombreposicion'],
                                 request.form['descripcion'])
        session.close()
        return redirect(url_for('listar_posicion'))
    else:
        return render_template('agregar_posicion.html')

@app.route('/posicion/editar/<int:idposicion>', methods=['GET', 'POST'])
def editar_posicion(idposicion):
    session = DBSession()
    if request.method == 'POST':
        Posicion.modificarPosicion(session, idposicion,
                                   nombreposicion=request.form['nombreposicion'],
                                   descripcion=request.form['descripcion'])
        session.close()
        return redirect(url_for('listar_posicion'))
    else:
        posicion = session.query(Posicion).filter_by(idposicion=idposicion).first()
        session.close()
        return render_template('editar_posicion.html', posicion=posicion)

@app.route('/posicion/eliminar/<int:idposicion>', methods=['POST'])
def eliminar_posicion(idposicion):
    session = DBSession()
    Posicion.eliminarPosicion(session, idposicion)
    session.close()
    return redirect(url_for('listar_posicion'))

# Rutas para Jugador
@app.route('/jugador')
def listar_jugador():
    session = DBSession()  # Abre una nueva sesión
    jugadores = session.query(Jugador).options(
        joinedload(Jugador.posicion),
        joinedload(Jugador.equipo)  # Carga la relación 'equipo' usando joinedload
    ).all()

    posiciones = session.query(Posicion).all()
    print(posiciones)
    for posicion in posiciones:
        print (posicion.nombreposicion)
    equipos= session.query(Equipo).all()
    

    session.close()  # Cierra la sesión después de obtener los datos
    
    return render_template('jugador.html', jugadores=jugadores, posiciones= posiciones, equipos=equipos)

@app.route('/jugador/agregar', methods=['GET', 'POST'])
def agregar_jugador():
    if request.method == 'POST':
        session = DBSession()
        print(request.form)
        Jugador.agregarJugador(session,
                               request.form['nombrejugador'],
                               request.form['edad'],
                               request.form['nacionalidad'],
                               request.form['idposicion'],
                               request.form['idequipo'])
        session.close()
        return redirect(url_for('listar_jugador'))
    else:
        session = DBSession()
        posiciones = session.query(Posicion).all()
        equipos = session.query(Equipo).all()
        
        session.close()
        return render_template('agregar_jugador.html', posiciones=posiciones, equipos=equipos)

@app.route('/jugador/editar/<int:idjugador>', methods=['GET', 'POST'])
def editar_jugador(idjugador):
    session = DBSession()
    if request.method == 'POST':
        Jugador.modificarJugador(session, idjugador,
                                 nombrejugador=request.form['nombrejugador'],
                                 edad=request.form['edad'],
                                 nacionalidad=request.form['nacionalidad'],
                                 idposicion=request.form['idposicion'],
                                 idequipo=request.form['idequipo'])
        session.close()
        return redirect(url_for('listar_jugador'))
    else:
        jugador = session.query(Jugador).filter_by(idjugador=idjugador).first()
        posiciones = session.query(Posicion).all()
        equipos = session.query(Equipo).all()
        session.close()
        return render_template('editar_jugador.html', jugador=jugador, posiciones=posiciones, equipos=equipos)

@app.route('/jugador/eliminar/<int:idjugador>', methods=['POST'])
def eliminar_jugador(idjugador):
    session = DBSession()
    Jugador.eliminarJugador(session, idjugador)
    session.close()
    return redirect(url_for('listar_jugador'))

if __name__ == '__main__':
    app.run(debug=True)
