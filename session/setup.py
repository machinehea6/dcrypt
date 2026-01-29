
from definitions import *
import os
class Setup():
    def __init__(self):
        is_setup = self._check_is_init()
        if not is_setup:
            self._gen_keys()

    def _check_is_init(self):
        key_files = os.listdir(f"{ROOT_DIR}/data/secrets")
        if len(key_files) < 2:
            return False
        else:
            return True
    
    def _gen_keys(self):
        priv_key = RSA.generate(3072)
        pub_key = priv_key.public_key()

        with open(f"{ROOT_DIR}/data/secrets/priv_key.pem", "wb") as f:
            data = priv_key.export_key()
            f.write(data)
        with open(f"{ROOT_DIR}/data/secrets/pub_key.pem", "wb") as f:
            data = pub_key.export_key()
            f.write(data)
    