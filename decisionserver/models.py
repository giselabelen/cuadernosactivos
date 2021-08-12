from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import *
from sqlalchemy.orm import relationship

engine = create_engine('sqlite:///EjerciciosCA.db', echo=True)

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class EjercicioPorGuia(Base):
	__tablename__ = 'ejerciciosPorGuia'

	id_guia = Column(Integer, primary_key=True)		# numero de guia
	id_ejercicio = Column(Integer,primary_key=True)	# numero de ejercicio de la guia
	ejercicio = Column(Text)						# ejercicio propiamente dicho
	solucion = Column(Text)							# respuesta correcta al ejercicio
	id_siguiente = Column(Integer)					# siguiente ejercicio de la guia


class ActividadPorAlumne(Base):
	__tablename__ = 'actividadesPorAlumne'

	id = Column(Integer, primary_key=True)	
	usuario = Column(String(128))	# usuario (por ahora, el valor que toma jupyter)
	timestamp = Column(DATETIME)	# timestamp del update
	id_guia = Column(Integer)		# numero de guia
	id_ejercicio = Column(Integer)	# numero de ejercicio de la guia
	resolucion = Column(Text)		# solucion propuesta por el usuario
	anotacion = Column(Text)		# anotacion opcional


class DesempenioPBPorEstudiante(Base):
	__tablename__ = 'desempenioPBPorEstudiante'

	id = Column(Integer, primary_key=True)
	usuario = Column(String(128))	# usuario (por ahora, el valor que toma jupyter)
	id_ejercicio = Column(Integer)	# identificador del ejercicio de PB
	outcome = Column(Float)			# resultado que devuelve PB


def create_all():
    Base.metadata.create_all(engine)