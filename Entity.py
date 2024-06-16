from sqlalchemy import Column, Integer, String, ForeignKey, Date, Numeric, Text, Sequence,DateTime,BINARY
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import func
Base= declarative_base()
class Equipo(Base):
    __tablename__='equipo'
    idequipo=Column(Integer, primary_key=True, autoincrement=True)
    nombreequipo=Column(String(50))
    anioofundacion=Column(Integer)
    estadio=Column(String(50))
    ciudad=Column(String(50))
    ##jugador=relationship('Jugador')
    @staticmethod
    def modificarEquipo(session, idequipo, **kwargs):
        equipo= session.query(Equipo).filter_by(idequipo=idequipo).first()
        if equipo:
            for key, value in kwargs.items():
                setattr(equipo, key,value)
            session.commit()
            print('Equipo Actualizado')
        else:
            print('Equipo no encontrado')
    @staticmethod
    def agregarEquipo(session,nombreequipo,anioofundacion,estadio,ciudad):
        nuevoEquipo=Equipo(nombreequipo=nombreequipo,anioofundacion=anioofundacion,estadio=estadio,ciudad=ciudad)
        session.add(nuevoEquipo)
        session.commit()
        print("Equipo agregado correctamente")
    @staticmethod
    def eliminarEquipo(session,idequipo):
        equipo=session.query(Equipo).filter_by(idequipo=idequipo).first()
        if equipo:
            session.delete(equipo)
            session.commit()
            print("Equipo eliminado")
        else:
            print("Equipo no encontrado")
class Posicion(Base):
    __tablename__='posicion'
    idposicion=Column(Integer, primary_key=True, autoincrement=True)
    nombreposicion=Column(String(50),nullable=False)
    descripcion=Column(Text)
    @staticmethod
    def modificarPosicion(session, idposicion, **kwargs):
        posicion= session.query(Posicion).filter_by(idposicion=idposicion).first()
        if posicion:
            for key, value in kwargs.items():
                setattr(posicion, key,value)
            session.commit()
            print('Posicion Actualizada')
        else:
            print('Posicion no encontrada')
    @staticmethod
    def agregarPosicion(session,nombreposicion,descripcion):
        nuevaPosicion=Posicion(nombreposicion=nombreposicion,descripcion=descripcion)
        session.add(nuevaPosicion)
        session.commit()
        print("Posicion agregada correctamente")
    @staticmethod
    def eliminarPosicion(session,idposicion):
        posicion=session.query(Posicion).filter_by(idposicion=idposicion).first()
        if posicion:
            session.delete(posicion)
            session.commit()
            print("Posicion eliminada")
        else:
            print("Posicion no encontrada")
class Jugador(Base):
    __tablename__='jugador'
    idjugador=Column(Integer, primary_key=True, autoincrement=True)
    nombrejugador=Column(String(50))
    edad=Column(Integer)
    nacionalidad=Column(String(50))
    idposicion=Column(Integer,ForeignKey('posicion.idposicion'))
    idequipo=Column(Integer,ForeignKey('equipo.idequipo'))
    posicion=relationship('Posicion')
    equipo=relationship('Equipo')
    @staticmethod
    def agregarJugador(session,nombrejugador,edad, nacionalidad,idposicion,idequipo):
        nuevo_jugador=Jugador(nombrejugador=nombrejugador, edad=edad, 
                              nacionalidad=nacionalidad, idposicion=idposicion,idequipo=idequipo)
        
        session.add(nuevo_jugador)
        session.commit()
        print('Se agregado un nuevo jugador')
    @staticmethod
    def modificarJugador(session, idjugador, **kwargs):
        jugador= session.query(Jugador).filter_by(idjugador=idjugador).first()
        if jugador:
            for key, value in kwargs.items():
                setattr(jugador, key,value)
            session.commit()
            print('Jugador Actualizado')
        else:
            print('Jugador no encontrado')
    @staticmethod
    def eliminarJugador(session,idjugador):
        jugador=session.query(Jugador).filter_by(idjugador=idjugador).first()
        if jugador:
            session.delete(jugador)
            session.commit()
            print("Jugador eliminado")
        else:
            print("Jugador no encontrado")
