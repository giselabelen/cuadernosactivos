import os

def _jupyter_nbextension_paths():
    return [
        dict(
            section="notebook",
            src=os.path.join('nbextension','check'),
            dest="corrector",
            require="check/check"
        )
    ]

def _jupyter_server_extension_paths():
    return [
        dict(
            module="serverextension.corrector"
        )
    ]

