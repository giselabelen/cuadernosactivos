from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler
from tornado import web

import requests

class CorrectorHandler(IPythonHandler):
    # def get(self):
    #     self.finish('Hello, world!')

    def post(self):
        print ("iniciando corrección")

        url = "http://localhost:80/corrector/"
        data = self.request.body

        response = requests.post(url,data=data)

        self.write(response)

        print("Listo")



def load_jupyter_server_extension(nb_server_app):
    """
    Called when the extension is loaded.

    Args:
        nb_server_app (NotebookWebApplication): handle to the Notebook webserver instance.
    """

    nb_server_app.log.info("Loading the Corrector serverextension sarasa")
    web_app = nb_server_app.web_app
    host_pattern = '.*$'
    route_pattern = url_path_join(web_app.settings['base_url'], '/corrector')
    nb_server_app.log.info(route_pattern)
    web_app.add_handlers(host_pattern, [(route_pattern, CorrectorHandler)])



def _jupyter_server_extension_paths():
    return [{
        "module": "corrector"
    }]