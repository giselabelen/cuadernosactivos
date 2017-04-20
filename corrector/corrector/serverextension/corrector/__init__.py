from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler
from tornado import web, httpclient, gen

import requests

class CorrectorHandler(IPythonHandler):
    # def get(self):
    #     self.finish('Hello, world!')

    # def handle_request(response):
    # '''callback needed when a response arrive'''
    # if response.error:
    #     print "Error:", response.error
    # else:
    #     print 'called'
    #     print response.body

    #@web.asynchronous 
    @gen.coroutine
    def post(self):
        print("adentro")
        destination = "http://localhost:80/corrector/"
        http_client = httpclient.AsyncHTTPClient()

        # print ("iniciando corrección")

        # nombre = self.get_argument("nombre")
        # ejercicio = self.get_argument("ejercicio")
        # respuesta = self.get_argument("respuesta")

        # print ("Evaluando respuesta")
        # if respuesta == "1":
        #     correccion = {"aprobo":True}
        # else:
        #     correccion = {"aprobo":False}

        # self.write(correccion)  

        # print("Listo")

        usuario = self.get_current_user()
        print(usuario)


        request = httpclient.HTTPRequest(destination, body=self.request.body, method='POST')
        response = yield http_client.fetch(request)
        print(response.body)
        self.write(response.body)






# def _jupyter_server_extension_paths():
#     return [
#         dict(
#             module="corrector"
#         )
#     ]


def load_jupyter_server_extension(nb_server_app):
    """
    Called when the extension is loaded.

    Args:
        nb_server_app (NotebookWebApplication): handle to the Notebook webserver instance.
    """
    web_app = nb_server_app.web_app
    nb_server_app.log.info("Loading the Corrector serverextension")
    
    host_pattern = '.*$'
    route_pattern = url_path_join(web_app.settings['base_url'], 'corrector')
    nb_server_app.log.info(route_pattern)
    web_app.add_handlers(host_pattern, [(route_pattern, CorrectorHandler)])
