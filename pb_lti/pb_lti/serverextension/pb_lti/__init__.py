from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler
from tornado import httpclient, httputil


class PBLTIHandler(IPythonHandler):
        
        def get(self):

            # url del server que toma decisiones
            destination = "http://localhost:82/pb_lti/"

            http_client = httpclient.HTTPClient()

            usuario = self.get_current_user()

            params = {"usuario": usuario.decode()}

            url = httputil.url_concat(destination,params)

            response = http_client.fetch(url)

            # se reenvia la respuesta obtenida hacia la nbextension
            self.write(response.body)


def load_jupyter_server_extension(nb_server_app):
    """
    Called when the extension is loaded.

    Args:
        nb_server_app (NotebookWebApplication): handle to the Notebook webserver instance.
    """
    web_app = nb_server_app.web_app
    nb_server_app.log.info("Loading the PB_LTI serverextension")
    
    host_pattern = '.*$'
    route_pattern = url_path_join(web_app.settings['base_url'], 'pb_lti')
    nb_server_app.log.info(route_pattern)
    web_app.add_handlers(host_pattern, [(route_pattern, PBLTIHandler)])
