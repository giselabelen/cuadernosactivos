#from tornado import httpserver
#from tornado import gen
from tornado.ioloop import IOLoop
import tornado.web
import json
import ast

from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import scoped_session, sessionmaker
from models import * # import the engine to bind



class BaseHandler(tornado.web.RequestHandler):

    def db(self):
        return self.application.db

    def options(self):
        # no body
        self.set_status(204)
        self.finish()


class AdHocHandler(BaseHandler):

    def post(self):

        print ("Obteniendo datos")
        
        # recupero el cuerpo del post y lo transformo a diccionario
        args = self.decode_argument(self.request.body)
        data = json.loads(json.dumps(ast.literal_eval(args)))
        
        # obtengo los datos del diccionario
        respuesta = data["respuesta"]

        print ("Evaluando respuesta")
        if respuesta == "1":
            correccion = {"aprobo":True}
        else:
            correccion = {"aprobo":False}

        self.write(correccion)   

        print ("Listo")


class SeguimientoHandler(BaseHandler):

    def post(self):

        print ("Obteniendo datos")
        
        # recupero el cuerpo del post y lo transformo a diccionario
        args = self.decode_argument(self.request.body)
        data = json.loads(json.dumps(ast.literal_eval(args)))
        
        # obtengo los datos del diccionario
        usuario = data["usuario"]
        id_guia = data["id_guia"]
        id_ejercicio = data["id_ejercicio"]
        resolucion = data["resolucion"]
        timestamp = int(data["timestamp"])/1000

        # cargo los datos de la actividad para este alumne
        if (id_ejercicio != "0") & (id_guia != "0"):
            nuevaAct = ActividadPorAlumne(usuario=usuario,\
                                        timestamp=datetime.fromtimestamp(timestamp),\
                                        id_guia=id_guia,\
                                        id_ejercicio=id_ejercicio,\
                                        resolucion=resolucion)

            query = self.db().query(ActividadPorAlumne.anotacion).\
                                filter(ActividadPorAlumne.id_guia == id_guia,\
                                    ActividadPorAlumne.id_ejercicio == id_ejercicio,\
                                    ActividadPorAlumne.usuario == usuario)

            # query = self.db().query(ActividadPorAlumne.anotacion, func.max(ActividadPorAlumne.anotacion)).\
            # filter(ActividadPorAlumne.id_guia == id_guia,\
            #     ActividadPorAlumne.id_ejercicio == id_ejercicio,\
            #     ActividadPorAlumne.usuario == usuario)

            if (query.count()>0): # no es la primera vez que hace esta guia
                nuevaAct.anotacion = int(max(query.all())._asdict()["anotacion"]) + 1   #esto se tiene que poder hacer mejor
            else:
                nuevaAct.anotacion = 1

            self.db().add(nuevaAct)
            self.db().commit()
        
        # busco y envio el ejercicio siguiente
        id_guia_prox = id_guia
        id_ejercicio_prox = 0
        ejercicio = ''

        if (id_ejercicio == "0") & (id_guia == "0"):
            id_guia_prox = 1
            id_ejercicio_prox = 1

        else:
            query = self.db().query(EjercicioPorGuia).\
                    filter(EjercicioPorGuia.id_guia == id_guia,\
                             EjercicioPorGuia.id_ejercicio == id_ejercicio)
            id_ejercicio_prox = query.one().id_siguiente

            if id_ejercicio_prox == -1: # se termino esta guia
               
                # analizo el desempenio
                cant_respuestas_bien = 0
                cant_respuestas_mal = 0
                
                queryRepeticion = self.db().query(ActividadPorAlumne.anotacion, func.max(ActividadPorAlumne.anotacion)).\
                                filter(ActividadPorAlumne.id_guia == id_guia,\
                                    ActividadPorAlumne.usuario == usuario)
                repeticion = int(queryRepeticion.scalar())

                query = self.db().query(EjercicioPorGuia, ActividadPorAlumne).\
                                    filter(EjercicioPorGuia.id_guia == ActividadPorAlumne.id_guia).\
                                    filter(EjercicioPorGuia.id_ejercicio == ActividadPorAlumne.id_ejercicio).\
                                    filter(EjercicioPorGuia.id_guia == id_guia).\
                                    filter(ActividadPorAlumne.usuario == usuario).\
                                    filter(ActividadPorAlumne.anotacion == repeticion)

                for sol_ok,sol_alu in query.all():
                    if sol_ok.solucion == sol_alu.resolucion:
                        cant_respuestas_bien += 1
                    else:
                        cant_respuestas_mal += 1

                # si le fue mal
                if cant_respuestas_mal >= cant_respuestas_bien:

                    if id_guia == '1': # si era la primera guia, le mando a repasar
                        ejercicio = "vamos a repasar un poco mas"
                    else:   # si era otra guia, le mando a hacer la anterior
                        id_guia_prox = int(id_guia) - 1
                        id_ejercicio_prox = 1
                
                # si le fue bien
                else:
                    if id_guia == '3': # si era la ultima guia, ya termino
                        ejercicio = "bien ahi, ya terminaste"
                    else:   # si era otra guia, le mando a hacer la siguiente
                        id_guia_prox = int(id_guia) + 1
                        id_ejercicio_prox = 1
         

        self.set_header('content-type','application/json')

        # si mando a repasar o ya termino
        if id_ejercicio_prox == -1:
            id_guia_prox = 0
            id_ejercicio_prox = 0

        # si mando otra guia
        else:
            query = self.db().query(EjercicioPorGuia).\
            filter(EjercicioPorGuia.id_guia == id_guia_prox,\
                     EjercicioPorGuia.id_ejercicio == id_ejercicio_prox)

            ejercicio = query.one().ejercicio
        
        respuesta = {
                        "ejercicio":ejercicio,
                        "id_guia":id_guia_prox,
                        "id_ejercicio":id_ejercicio_prox   
                    }

        self.write(respuesta)

        print ("Listo")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/adhoc/?", AdHocHandler),
            (r"/seguimiento/?",SeguimientoHandler)
        ]
        tornado.web.Application.__init__(self, handlers)
        # Have one global connection.
        self.db = scoped_session(sessionmaker(bind=engine))
        create_all()


def main():

    app = Application()
    app.listen(82)
    IOLoop.instance().start()

if __name__ == '__main__':
    main()