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
from xml.etree import ElementTree as etree



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

        # cargo los datos de la actividad para este estudiante
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


class PBLTIHandler(BaseHandler):

    def get(self):  
        
        # obtengo nombre de usuario
        usuario = self.get_argument("usuario")

        # obtengo ejercicio (hardcodeado por ahora)
        ejercicio = 1 

        # obtengo id en la base de datos de notas para este usr y este ej
        query = self.db().query(DesempenioPBPorEstudiante).\
            filter(DesempenioPBPorEstudiante.usuario == usuario,\
                    DesempenioPBPorEstudiante.id_ejercicio == ejercicio)

        if (query.count()==1): # ya existe un registro para este usr-ej
            identif = query.one().id
        else:
            nuevoRegistro = DesempenioPBPorEstudiante(usuario=usuario, id_ejercicio=ejercicio)
            self.db().add(nuevoRegistro)
            self.db().commit()
            identif = nuevoRegistro.id
        
        # todo lo que voy a enviar para el lti launch
        json_data = {"usuario":usuario, "ejercicio": ejercicio, "identif": identif}

        
        # # por cross-domain
        # self.add_header("Access-Control-Allow-Origin","http://localhost:8888")
        
        self.write(json_data)

        # print ("Listo")


class OutcomesHandler(BaseHandler):

    def post(self):
        print ("Obteniendo datos")

        # namespaces del xml input
        ns = {'ns':'http://www.imsglobal.org/services/ltiv1p1/xsd/imsoms_v1p0'}

        # nodo raiz del xml input
        req_tree = etree.fromstring(self.request.body)
        
        # message id del xml input
        req_msg_id_node = req_tree.find('ns:imsx_POXHeader/ns:imsx_POXRequestHeaderInfo/ns:imsx_messageIdentifier',ns)
        req_msg_id = req_msg_id_node.text

        # nodo operacion del xml input 
        # reviso que sea replaceResult
        req_oper_node = req_tree.find('ns:imsx_POXBody/ns:replaceResultRequest',ns)
        if req_oper_node is None : # si no era replaceResult
            # veo si es read o delete
            code_major = 'unsopported'
            req_oper_read = req_tree.find('ns:imsx_POXBody/ns:readResultRequest',ns)
            req_oper_delete = req_tree.find('ns:imsx_POXBody/ns:deleteResultRequest',ns)

            if req_oper_read is not None: # si es read
                req_oper = 'readResult'
                severity = 'status'

            elif req_oper_delete is not None: # si es delete
                req_oper = 'deleteResult'
                severity = 'status'

            else: # si no es read ni delete
                req_oper = 'unknown' # esto podria ser mas declarativo... otro dia
                severity = 'error'

        else: # si era replaceResult
            code_major = 'success'
            severity = 'status'
            req_oper = 'replaceResult'

            # sourcedid, donde voy a guardar la nota recibida
            req_sourcedid_node = req_oper_node.find('ns:resultRecord/ns:sourcedGUID/ns:sourcedId',ns)
            req_sourcedid = req_sourcedid_node.text

            # nota recibida
            req_result_node = req_oper_node.find('ns:resultRecord/ns:result/ns:resultScore/ns:textString',ns)
            req_result = req_result_node.text

            # chequeo que la nota sea numerica decimal entre 0 y 1
            try:
                val = float(req_result)
                if not (0 <= val <= 1.0):
                    code_major = 'faliure'
                else:
                    # guardo la nota
                    entradaDesempenios = self.db().query(DesempenioPBPorEstudiante).get(req_sourcedid)
                    entradaDesempenios.outcome = val
                    self.db().commit()
                    pass
            except ValueError:
                code_major = "faliure"

        # nuestra respuesta
        xml_response = armar_xml(code_major,severity,req_msg_id,req_oper)

        self.write(xml_response)   
        self.set_header('Content-Type', 'text/xml')

        print ("Listo")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/adhoc/?", AdHocHandler),
            (r"/seguimiento/?",SeguimientoHandler),
            (r"/pb_lti/?",PBLTIHandler),
            (r"/outcomes/?", OutcomesHandler)
        ]
        tornado.web.Application.__init__(self, handlers)
        # Have one global connection.
        self.db = scoped_session(sessionmaker(bind=engine))
        create_all()


def armar_xml(code_major,severity,req_msg_id,req_oper):
    root = etree.Element(u'imsx_POXEnvelopeResponse',
                 xmlns=u'http://www.imsglobal.org/services/'
                       u'ltiv1p1/xsd/imsoms_v1p0')

    header = etree.SubElement(root, 'imsx_POXHeader')
    header_info = etree.SubElement(header, 'imsx_POXResponseHeaderInfo')
    version = etree.SubElement(header_info, 'imsx_version')
    version.text = 'V1.0'
    # message_identifier = etree.SubElement(header_info,
    #                                       'imsx_messageIdentifier')
    # message_identifier.text = message_identifier_id
    status_info = etree.SubElement(header_info,'imsx_statusInfo')
    code_major_node = etree.SubElement(status_info,'imsx_codeMajor')
    code_major_node.text = code_major
    severity_node = etree.SubElement(status_info,'imsx_severity')
    severity_node.text = severity
    message_ref_identifier = etree.SubElement(status_info,'imsx_messageRefIdentifier')
    message_ref_identifier.text = req_msg_id
    operation_ref_identifier = etree.SubElement(status_info,'imsx_operationRefIdentifier')
    operation_ref_identifier.text = req_oper

    body = etree.SubElement(root, 'imsx_POXBody')
    replace_result_response = etree.SubElement(body, 'replaceResultResponse')

    ret = "<?xml version='1.0' encoding='utf-8'?>\n{}".format(
        etree.tostring(root, encoding='utf-8'))

    # print("XML Response: \n%s", ret)
    return ret


def main():

    app = Application()
    app.listen(82)
    IOLoop.instance().start()

if __name__ == '__main__':
    main()