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
        # print (self.request.body)   

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
        code_major = etree.SubElement(status_info,'imsx_codeMajor')
        code_major.text = 'success'
        severity = etree.SubElement(status_info,'imsx_severity')
        severity.text = 'status'
        #message_ref_identifier = etree.SubElement(status_info,'imsx_messageRefIdentifier')
        operation_ref_identifier = etree.SubElement(status_info,'imsx_operationRefIdentifier')
        operation_ref_identifier.text = 'replaceResult'

        body = etree.SubElement(root, 'imsx_POXBody')
        replace_result_response = etree.SubElement(body, 'replaceResultResponse')

        ret = "<?xml version='1.0' encoding='utf-8'?>\n{}".format(
            etree.tostring(root, encoding='utf-8'))

        print("XML Response: \n%s", ret)
        #return ret

        # tipo = self.get_argument("lti_message_type")
        # sourcedid = self.get_argument("sourcedid")
        # score = self.get_argument("result_resultscore_textstring")
        
        # tipo = data[0]
        # sourcedid = data[1]
        # score = data[2]

        # print ("tipo:"+tipo)
        # print ("sourcedid:"+sourcedid)
        # print ("score:"+score)

        # print ("Guardando datos")
        # _execute("INSERT INTO resultados (nombre,ejercicio,respuesta) VALUES ('{0}','{1}','{2}')".format(nombre,ejercicio,respuesta))

        # print ("Evaluando respuesta")
        # if respuesta == "1":
        #     correccion = {"aprobo":True}
        # else:
        #     correccion = {"aprobo":False}

        # por cross-domain
#        self.add_header("Access-Control-Allow-Origin","http://localhost:8888")
        self.write(ret)   
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


def main():

    # Verify the database exists and has the correct layout
    verifyDatabase()

    app = Application()
    app.listen(82)
    IOLoop.instance().start()

if __name__ == '__main__':
    main()