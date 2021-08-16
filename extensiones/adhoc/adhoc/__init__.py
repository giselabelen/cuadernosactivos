import os

def _jupyter_nbextension_paths():
    return [
        dict(
            section="notebook",
            src=os.path.join('nbextension','adhoc'),
            dest="adhoc",
            require="adhoc/adhoc"
        )
    ]

def _jupyter_server_extension_paths():
    return [
        dict(
            module="adhoc.serverextension.adhoc"
        )
    ]

