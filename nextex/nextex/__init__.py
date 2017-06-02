import os
#import nbextension.check.check
#import serverextension.corrector

def _jupyter_nbextension_paths():
    return [
        dict(
            section="notebook",
            src=os.path.join('nbextension','nextex'),
            dest="nextex",
            require="nextex/nextex"
        )
    ]

def _jupyter_server_extension_paths():
    return [
        dict(
            module="nextex.serverextension.nextex"
        )
    ]

