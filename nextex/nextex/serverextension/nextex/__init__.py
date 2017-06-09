from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler
from tornado import web, httpclient, gen

import requests
import json

class NextExHandler(IPythonHandler):

    # @gen.coroutine
    # def post(self):

    #     destination = "http://localhost:82/corrector/"
    #     http_client = httpclient.AsyncHTTPClient()

    #     usuario = self.get_current_user()
    #     print(usuario)

    #     request = httpclient.HTTPRequest(destination, body=self.request.body, method='POST')
    #     response = yield http_client.fetch(request)
    #     print(response.body)
    #     self.write(response.body)


    @gen.coroutine
    def get(self):  

        destination = "http://localhost:82/corrector/"  # quedo nombre 'corrector' xq es el que usamos para la POC anterior
        http_client = httpclient.AsyncHTTPClient()

        usuario = self.get_current_user()
        print(usuario)
        
        # body = self.request.body #agregar usuario
        body = json.dumps({'usuario': usuario.decode()})


        request = httpclient.HTTPRequest(destination, body=body)
        response = yield http_client.fetch(request)
        print(response.body)
        self.write(response.body)
        


def load_jupyter_server_extension(nb_server_app):
    """
    Called when the extension is loaded.

    Args:
        nb_server_app (NotebookWebApplication): handle to the Notebook webserver instance.
    """
    web_app = nb_server_app.web_app
    nb_server_app.log.info("Loading the NextEx serverextension")
    
    host_pattern = '.*$'
    route_pattern = url_path_join(web_app.settings['base_url'], 'nextex')
    nb_server_app.log.info(route_pattern)
    web_app.add_handlers(host_pattern, [(route_pattern, NextExHandler)])
