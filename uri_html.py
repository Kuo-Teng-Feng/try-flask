import os
import pathlib

def uri(filename):
        
    return pathlib.Path(os.path.abspath("templates")).as_uri() + f"/{filename}"
