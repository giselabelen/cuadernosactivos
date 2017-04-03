from tornado import httpserver
from tornado import gen
from tornado.ioloop import IOLoop
import sqlite3 as sqlite
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello, world')

class CarHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('GET - Welcome to the CarHandler!')

    def post(self):
        self.write('POST - Welcome to the CarHandler!')

def verifyDatabase():
    conn = sqlite.connect('cars.db')
    c = conn.cursor()
    try:
        c.execute('SELECT * FROM cars')
        print('Table already exists')
    except:
        print('Creating table \'cars\'')
        c.execute('CREATE TABLE cars (\
            id text,\
            make text,\
            model text,\
            year text,\
            trans text,\
            color text)')
        print('Successfully created table \'cars\'')
    conn.commit()
    conn.close()

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/?", MainHandler),
            (r"/api/v1/cars/?", CarHandler),
            (r"/api/v1/cars/[0-9][0-9][0-9][0-9]/?", CarHandler)
        ]
        tornado.web.Application.__init__(self, handlers)

def main():

    # Verify the database exists and has the correct layout
    verifyDatabase()

    app = Application()
    app.listen(80)
    IOLoop.instance().start()

if __name__ == '__main__':
    main()