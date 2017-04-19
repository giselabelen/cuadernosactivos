from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler
from tornado import web, httpclient

import requests

class CorrectorHandler(IPythonHandler):
    # def get(self):
    #     self.finish('Hello, world!')

    def handle_request(response):
    '''callback needed when a response arrive'''
    if response.error:
        print "Error:", response.error
    else:
        print 'called'
        print response.body

    #@web.asynchronous 
    def post(self):
    
        destination = "http://localhost:80/corrector/"
        http_client = httpclient.AsyncHTTPClient()

        # print ("iniciando corrección")

        # url = "http://localhost:80/corrector/"
        # data = self.request.body
        # print(data)

        # response = requests.post(url,data=data)
        # print(response)

        # self.write(response)

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

        request = httpclient.HTTPRequest(destination, body=self.request.body, method='POST')
        http_client.fetch(request,handle_request) # OJO QUE ESTO NO ANDA
        #print(response.request)
        #print(response.code)
        #print(response.reason)
        #print(response.headers)
        #print(response.effective_url)
        #print(response.body)
        #print(response.error)
        # self.write(response)






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
