#from tornado import httpserver
#from tornado import gen
from tornado.ioloop import IOLoop
import sqlite3 as sqlite
import tornado.web
import json
import ast
#import xmltodict
#from xml.etree import ElementTree as etree

class BaseHandler(tornado.web.RequestHandler):

    #def set_default_headers(self):
        # print("setting headers!!!")
        # self.set_header("Access-Control-Allow-Origin", "*")
        # self.set_header("Access-Control-Allow-Headers", "Authorization, content-type")
        # self.set_header('Access-Control-Allow-Methods', 'OPTIONS')

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
        #print(data)
        # obtengo los datos del diccionario
        nombre = data["usuario"]
        ejercicio = data["ejercicio"]
        respuesta = data["respuesta"]

        # guardo los datos en la base de datos
        print ("Guardando datos")
        _execute("INSERT INTO resultados (nombre,ejercicio,respuesta) VALUES ('{0}','{1}','{2}')".format(nombre,ejercicio,respuesta))

        # evaluo la respuesta del alumno y la envio
        print ("Evaluando respuesta")
        if respuesta == "1":
            correccion = {"aprobo":True}
        else:
            correccion = {"aprobo":False}

        self.write(correccion)   

        print ("Listo")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/adhoc/?", AdHocHandler)
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

    try:
        _execute('SELECT * FROM resultados')
        print('Table already exists')
    except:
        print('Creating table \'resultados\'')

        _execute('CREATE TABLE resultados (\
            nombre text,\
            ejercicio text,\
            respuesta text)')
        print('Successfully created table \'resultados\'')



def main():

    # Verify the database exists and has the correct layout
    verifyDatabase()

    app = Application()
    app.listen(82)
    IOLoop.instance().start()

if __name__ == '__main__':
    main()