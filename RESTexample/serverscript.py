from tornado import httpserver
from tornado import gen
from tornado.ioloop import IOLoop
import sqlite3 as sqlite
import tornado.web
import json
#import xmltodict
from xml.etree import ElementTree as etree

class CorrectorHandler(tornado.web.RequestHandler):
    # def prepare(self):
    #     if self.request.headers["Content-Type"].startswith("application/json"):
    #         print('if')
    #         self.json_args = json.loads(self.request.body)
    #     else:
    #         print('else')
    #         self.json_args = None

    def post(self):
        print ("Obteniendo datos")
        #print (self.request.body)
        nombre = self.get_argument("nombre")
        ejercicio = self.get_argument("ejercicio")
        respuesta = self.get_argument("respuesta")
        #print (nombre + ejercicio + respuesta)
        # data = tornado.escape.json_decode(self.request.body)
        # nombre = data["nombre"]
        # ejercicio = data["ejercicio"]
        # respuesta = data["respuesta"]

        print ("Guardando datos")
        _execute("INSERT INTO resultados (nombre,ejercicio,respuesta) VALUES ('{0}','{1}','{2}')".format(nombre,ejercicio,respuesta))

        print ("Evaluando respuesta")
        if respuesta == "1":
            correccion = {"aprobo":True}
        else:
            correccion = {"aprobo":False}

        # por cross-domain
        self.add_header("Access-Control-Allow-Origin","http://localhost:8888")
        self.write(correccion)   

        print ("Listo")


    def get(self):  
        print ("Analizando")
        #print (json.loads(self.request.body))
        usuario = self.get_argument("usuario")
        print(usuario)
        #usuario = json.loads(self.request.body)['usuario']

        #json_data = json.loads(self.request.body)
        #json_data["ejercicio"] = 1
        json_data = {"usuario":usuario, "ejercicio": 1}

        
        # por cross-domain
        self.add_header("Access-Control-Allow-Origin","http://localhost:8888")
        #self.write(self.request.body)   
        self.write(json_data)

        print ("Listo")


class OutcomesHandler(tornado.web.RequestHandler):

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
                    # hacer lo correspondiente para guardar la nota
                    pass
            except ValueError:
                code_major = "faliure"

        # nuestra respuesta
        xml_response = armar_xml(code_major,severity,req_msg_id,req_oper)

        # print ("Guardando datos")
        # _execute("INSERT INTO resultados (nombre,ejercicio,respuesta) VALUES ('{0}','{1}','{2}')".format(nombre,ejercicio,respuesta))

        self.write(xml_response)   
        self.set_header('Content-Type', 'text/xml')

        print ("Listo")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/corrector/?", CorrectorHandler),
            (r"/outcomes/?", OutcomesHandler)
        ]
        tornado.web.Application.__init__(self, handlers)


def _execute(query):
    """Function to execute queries against a local sqlite database"""
    dbPath = 'resultados.db'
    connection = sqlite.connect(dbPath)
    cursorobj = connection.cursor()
    try:
            cursorobj.execute(query)
            result = cursorobj.fetchall()
            connection.commit()
    except Exception:
            raise
    connection.close()
    return result


def verifyDatabase():
    # conn = sqlite.connect('resultados.db')
    # c = conn.cursor()
    try:
        #c.execute('SELECT * FROM resultados')
        _execute('SELECT * FROM resultados')
        print('Table already exists')
    except:
        print('Creating table \'resultados\'')
        # c.execute('CREATE TABLE resultados (\
        #     nombre text,\
        #     ejercicio text,\
        #     respuesta text)')
        _execute('CREATE TABLE resultados (\
            nombre text,\
            ejercicio text,\
            respuesta text)')
        print('Successfully created table \'resultados\'')
    # conn.commit()
    # conn.close()


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

    # Verify the database exists and has the correct layout
    verifyDatabase()

    app = Application()
    app.listen(82)
    IOLoop.instance().start()

if __name__ == '__main__':
    main()