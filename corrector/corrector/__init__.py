import os
#import nbextension.check.check
#import serverextension.corrector

def _jupyter_nbextension_paths():
    return [
        dict(
            section="notebook",
            src=os.path.join('nbextension','check'),
            dest="corrector",
            require="corrector/check"
        )
    ]

def _jupyter_server_extension_paths():
    return [
        dict(
            module="corrector.serverextension.corrector"
        )
    ]

