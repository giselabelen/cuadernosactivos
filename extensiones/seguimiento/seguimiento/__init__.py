import os

def _jupyter_nbextension_paths():
    return [
        dict(
            section="notebook",
            src=os.path.join('nbextension','seguimiento'),
            dest="seguimiento",
            require="seguimiento/seguimiento"
        )
    ]

def _jupyter_server_extension_paths():
    return [
        dict(
            module="seguimiento.serverextension.seguimiento"
        )
    ]

