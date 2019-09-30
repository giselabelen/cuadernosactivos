import os

def _jupyter_nbextension_paths():
    return [
        dict(
            section="notebook",
            src=os.path.join('nbextension','pb_lti'),
            dest="pb_lti",
            require="pb_lti/pb_lti"
        )
    ]

def _jupyter_server_extension_paths():
    return [
        dict(
            module="pb_lti.serverextension.pb_lti"
        )
    ]
