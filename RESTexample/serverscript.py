from tornado import httpserver
from tornado import gen
from tornado.ioloop import IOLoop
import sqlite3 as sqlite
import tornado.web
import json


class CorrectorHandler(tornado.web.RequestHandler):
    def prepare(self):
        if self.request.headers["Content-Type"].startswith("application/json"):
            self.json_args = json.loads(self.request.body)
        else:
            self.json_args = None

    def post(self):
        print "Guardando datos"
        nombre = self.json_args["nombre"]
        ejercicio = self.json_args["ejercicio"]
        respuesta = self.json_args["respuesta"]
        _execute("INSERT INTO resultados (nombre,ejercicio,respuesta) VALUES ('{0}','{1}','{2}')".format(nombre,ejercicio,respuesta))

        print "Evaluando respuesta"
        if respuesta == "1":
            correccion = {"aprobo":True}
        else:
            correccion = {"aprobo":False}
        self.write(correccion)   

        print "Listo"


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/corrector/?", CorrectorHandler)
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
    app.listen(80)
    IOLoop.instance().start()

if __name__ == '__main__':
    main()