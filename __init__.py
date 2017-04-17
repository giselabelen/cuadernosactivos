import os

def _jupyter_nbextension_paths():
    return [
        dict(
            section="notebook",
            src=os.url_path_join('nbextensions','check'),
            dest="check",
            require="check/check"
        )
    ]

