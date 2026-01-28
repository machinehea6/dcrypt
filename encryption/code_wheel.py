from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from chat import *
import json 
import definitions
from dotenv import load_dotenv, dotenv_values
import os

class Encryption():
    def __init__(self):
        #chat = self.chat
        return

    def first_time_setup(self):
        cryptographer = Encryption()
        my_keys = cryptographer.gen_pair()
        try:
            os.environ['priv'] = my_keys['priv']
            os.environ['pub'] = my_keys['pub']
        except PermissionError:
            print(f"Permission error on {ROOT_DIR}")
            sys.exit()

    def is_setup(self):
        return 
    def get_conf_info(self):
        return
        
    def _gen_pair(self) -> dict:
        key = RSA.generate(2048)
        private_key = key.export_key()

        public_key = key.public_key().export_key()

        return {'pub':public_key, 'priv':private_key}
    
    def decrypt_msg(message:chat.Message):
        body = message.message_body.encode('utf-8')


