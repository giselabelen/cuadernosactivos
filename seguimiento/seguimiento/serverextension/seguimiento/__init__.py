from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler
from tornado import httpclient


class SeguimientoHandler(IPythonHandler):
        
    def post(self):

        # url del server que toma decisiones
        destination = "http://localhost:82/seguimiento/"

        http_client = httpclient.HTTPClient()

        usuario = self.get_current_user()
    
        # se van a enviar los datos provistos en el cuerpo del post mas el nombre de usuario        
        params = {  "usuario": usuario.decode(),
                    "id_guia" : self.get_argument("id_guia"),
                    "id_ejercicio" : self.get_argument("id_ejercicio"),
                    "resolucion": self.get_argument("resolucion"),
                    "timestamp" : self.get_argument("timestamp")
          }

        request = httpclient.HTTPRequest(destination, body=str(params), method='POST')

        response = http_client.fetch(request)
    
        # se reenvia la respuesta obtenida hacia la nbextension
        self.write(response.body)



def load_jupyter_server_extension(nb_server_app):
    """
    Called when the extension is loaded.

    Args:
        nb_server_app (NotebookWebApplication): handle to the Notebook webserver instance.
    """
    web_app = nb_server_app.web_app
    nb_server_app.log.info("Loading the Seguimiento serverextension")
    
    host_pattern = '.*$'
    route_pattern = url_path_join(web_app.settings['base_url'], 'seguimiento')
    nb_server_app.log.info(route_pattern)
    web_app.add_handlers(host_pattern, [(route_pattern, SeguimientoHandler)])
